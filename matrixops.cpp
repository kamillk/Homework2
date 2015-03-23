#include <vector>

extern "C" {
#include <Python.h>
}

using namespace std;

static PyObject * floyd_warshall(PyObject* module, PyObject* args)
{
	int i, j, k;
	PyObject * input_matrix = PyTuple_GetItem(args, 0);
	int vertex_number = PyObject_Length(input_matrix);
	vector<vector<double> > d(vertex_number, vector<double>(vertex_number));

	for (i = 0; i < vertex_number; i++)
	{
		PyObject * row = PyList_GetItem(input_matrix, i);
		for (j = 0; j < vertex_number; j++)
			d[i][j] = PyFloat_AsDouble(PyList_GetItem(row, j));
	}

	for (k = 0; k < vertex_number; k++)
		for (i = 0; i < vertex_number; i++)
			for (j = 0; j < vertex_number; j++)
			{
				if (d[i][j] == 0 || d[i][k] == 0 && d[k][j] == 0)
					d[i][j] = 0;
				else
					d[i][j] = 1.0 / (1.0 / d[i][j] + 1.0 / (d[i][k] + d[k][j]));
			}

	PyObject * output_matrix = PyList_New(vertex_number);
	for (i = 0; i < vertex_number; i++)
	{
		PyObject * row = PyList_New(vertex_number);
		PyList_SetItem(output_matrix, i, row);
		for (int j = 0; j < vertex_number; j++)
		{
			PyObject * py_elem = PyFloat_FromDouble(d[i][j]);
			PyList_SetItem(row, j, py_elem);
		}
	}

	
	return output_matrix;
}


PyMODINIT_FUNC PyInit_matrixops()
{
	static PyMethodDef ModuleMethods[] = {
		{ "floyd_warshall", floyd_warshall, METH_VARARGS, "floyd_warshall" },
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"matrixops",
		"Graph",
		-1, ModuleMethods, 
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
