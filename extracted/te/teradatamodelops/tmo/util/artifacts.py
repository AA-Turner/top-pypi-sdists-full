from tmo import ModelContext


def save_plot(title: str, dpi: int = 500, context: ModelContext = None):
    """
    This assumes the plot has already been rendered, and we only need to save it.
    :param title: the title of the plot and the file name to save as (spaces replaced with _ and all lower)
    :param dpi: the dpi setting
    :param context: ModelContext
    :return: None
    """
    import matplotlib.pyplot as plt

    plt.title(title)
    fig = plt.gcf()
    title = title.replace(" ", "_").lower()

    filename = f"artifacts/output/{title}"
    if context:
        filename = f"{context.artifact_output_path}/{title}"

    fig.savefig(filename, dpi=dpi)
    plt.clf()
