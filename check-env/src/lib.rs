use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::exceptions::PyValueError;
use std::env;

struct PyVarError {
    msg: String
}

impl std::convert::From<PyVarError> for PyErr {
    fn from(err: PyVarError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}


impl std::fmt::Display for PyVarError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.msg)
    }
}

fn get_env_var() -> Result<String, PyVarError> {
    match env::var("DATA_DIR") {
        Ok(val) => Ok(val.to_string()),
        Err(e) => Err(PyVarError{ msg: e.to_string() })
    }
}

#[pyfunction]
fn get_data_dir() -> PyResult<String> {
    Ok(get_env_var()?)
}

#[pyfunction]
fn check_bool() -> PyResult<bool> {
    Ok(!env::var("DEBUG").is_err())
}

#[pymodule]
fn check_env(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_data_dir, m)?)?;
    m.add_function(wrap_pyfunction!(check_bool, m)?)?;

    Ok(())
}
