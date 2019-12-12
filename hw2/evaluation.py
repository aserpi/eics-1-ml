from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


def plot_metrics(net, history):
    metrics = pd.read_csv(history)
    metrics.index += 1

    metrics.rename(columns={"acc": "Accuracy",
                            "loss": "Loss",
                            "val_acc": "Validation accuracy",
                            "val_loss": "Validation loss"},
                   inplace=True)

    plt.figure()
    ax = sns.lineplot(data=metrics[["Accuracy", "Validation accuracy"]], dashes=False, markers=True)
    ax.set(xlabel="Epoch", ylabel='Accuracy')
    ax.get_figure().savefig(history.parent / f"{net}_accuracy.pdf", format="pdf")
    plt.clf()

    plt.figure()
    ax = sns.lineplot(data=metrics[["Loss", "Validation loss"]], dashes=False, markers=True)
    ax.set(xlabel="Epoch", ylabel="Loss")
    ax.get_figure().savefig(history.parent / f"{net}_loss.pdf", format="pdf")
    plt.clf()


plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = []
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = [r"\usepackage{lmodern}"]
