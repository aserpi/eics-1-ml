import pandas as pd
import pickle
import os

from hw1.classifiers import classifier


def learn(X, y, algs, out):
    classes = pd.unique(y)

    for alg in algs:
        print(f"\nFitting {alg}...", end="\t")
        clf, partial_fit = classifier(alg)

        # X is too big to fit in memory: partial fits
        if partial_fit and len(X) * len(X.columns) > 350000000:
            try:
                with open(f"{out}/{alg}_batch.zip", "rb") as fin_batch, \
                        open(f"{out}/{alg}.zip", "rb") as fin_classifier:
                    (batches, first_batch) = pickle.load(fin_batch)
                    clf = pickle.load(fin_classifier)
            except (FileNotFoundError, TypeError):
                batches = int(len(X) / 645)
                first_batch = 0
            print("")

            for i in range(first_batch, batches):
                start_idx = int(len(X) / batches * i)
                end_idx = int(len(X) / batches * (i + 1)) - 1
                print(f"Fitting partition {i + 1} of {batches}...", end="\t")
                clf.partial_fit(X[start_idx:end_idx], y[start_idx:end_idx], classes=classes)

                with open(f"{out}/{alg}.zip", "wb") as fout_classifier:
                    pickle.dump(clf, fout_classifier, protocol=pickle.HIGHEST_PROTOCOL)
                with open(f"{out}/{alg}_batch.zip", "wb") as fout_batch:
                    pickle.dump((batches, i + 1), fout_batch, protocol=pickle.HIGHEST_PROTOCOL)
                print("Done.")

            os.remove(f"{out}/{alg}_batch.zip")

        # X fits in memory: direct computation
        else:
            clf.fit(X, y)
            with open(f"{out}/{alg}.zip", "wb") as fout_classifier:
                pickle.dump(clf, fout_classifier, protocol=pickle.HIGHEST_PROTOCOL)
            print("Done.")
