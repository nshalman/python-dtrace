#include <Python.h>
#include <usdt.h>
#include <string.h>
#include <stdio.h>

static PyObject *usdtError = NULL;

usdt_provider_t	*global_provider = NULL;
usdt_probedef_t *the_probe = NULL;

static PyObject* provider(PyObject* self, PyObject* args)
{
  char *name;
  char *module;

  if (!PyArg_ParseTuple(args, "ss", &name, &module))
    Py_RETURN_FALSE;

	if ((global_provider = usdt_create_provider(name, module)) == NULL)
		Py_RETURN_FALSE;

	Py_RETURN_TRUE;
}

static PyObject* simple_probe(PyObject* self, PyObject* args)
{
  char *probefunc;
  char *probename;
	char *probe_args[] = { "char *" };


  if (!PyArg_ParseTuple(args, "ss", &probefunc, &probename))
    Py_RETURN_FALSE;

	if ((the_probe = usdt_create_probe(probefunc, probename, 1, (void**)probe_args )) == NULL)
		Py_RETURN_FALSE;


	usdt_provider_add_probe(global_provider, the_probe);

	if ((usdt_provider_enable(global_provider)) < 0) {
		fprintf(stderr, "unable to enable provider: %s\n", usdt_errstr(global_provider));
	}

	if ((usdt_provider_enable(global_provider)) < 0)
		Py_RETURN_FALSE;

	Py_RETURN_TRUE;
}

static PyObject* fire(PyObject* self, PyObject* args)
{
  char *argument;
	char *probe_args[1];

  if (!PyArg_ParseTuple(args, "s", &argument))
    Py_RETURN_FALSE;

	probe_args[0] = argument;

	if (usdt_is_enabled(the_probe->probe))
		usdt_fire_probe(the_probe->probe, 1, (void**)probe_args);

	Py_RETURN_TRUE;
}

PyMethodDef usdt_methods[] = {
  {"provider", provider, METH_VARARGS},
  {"simple_probe", simple_probe, METH_VARARGS},
  {"fire", fire, METH_VARARGS},
  {NULL, NULL},
};

PyMODINIT_FUNC
initdtrace()
{
  PyObject *m;

  m = Py_InitModule("dtrace", usdt_methods);
  if (m == NULL)
    return;

  usdtError = PyErr_NewException("usdt.error", NULL, NULL);
  Py_INCREF(usdtError);
  PyModule_AddObject(m, "error", usdtError);
}
