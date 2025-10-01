import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def run_notebook(notebook_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='venv_python')
    ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})

    print(f'Notebook \"{notebook_path}\" executado com sucesso.')

if __name__ == "__main__":
    notebook_file = os.path.join('notebooks', 'iot_challenge_mottu.ipynb')
    run_notebook(notebook_file)
