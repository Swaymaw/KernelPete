from src.modules.kernel_manager import KernelEngine

if __name__ == "__main__":
    img_exp = """
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3], [1, 1, 1])
        plt.show()
        """

    pandas_exp = """
        import pandas as pd
        df = pd.DataFrame({"a": [1, 2, 3], "b": [1, 1, 1]})
        df.head()
    """

    ke = KernelEngine(kernel_name="testing_auto", notebook_path="generated_notebooks/testing.ipynb")
    ke.execute(img_exp)
    ke.execute(pandas_exp)
