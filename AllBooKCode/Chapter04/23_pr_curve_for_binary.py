import numpy as np
from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def predict(y_scores, threholds):
    return (y_scores >= threholds) * 1


def compute_scores(y_true, y_pred):
    p_score = precision_score(y_true, y_pred)
    r_score = recall_score(y_true, y_pred)
    return p_score, r_score


def p_r_curve(y_true, y_scores):
    thresholds = sorted(np.unique(y_scores))
    precisions, recalls = [], []
    for thre in thresholds:
        y_pred = predict(y_scores, thre)
        r = compute_scores(y_true, y_pred)
        precisions.append(r[0])
        recalls.append(r[1])

    last_ind = np.searchsorted(recalls[::-1], recalls[0]) + 1
    precisions = precisions[-last_ind:]
    recalls = recalls[-last_ind:]
    thresholds = thresholds[-last_ind:]

    precisions.append(1)
    recalls.append(0)
    return precisions, recalls, thresholds


def compute_ap(recall, precision):
    # \\text{AP} = \\sum_n (R_n - R_{n-1}) P_n
    rp = [item for item in zip(recall, precision)][::-1]  # 按recall升序进行排序
    ap = 0
    for i in range(1, len(rp)):
        ap += (rp[i][0] - rp[i - 1][0]) * rp[i][1]
    return round(ap, 2)


def get_dataset():
    x, y = load_iris(return_X_y=True)
    random_state = np.random.RandomState(2020)
    n_samples, n_features = x.shape
    # 为数据增加噪音维度以便更好观察pr曲线
    x = np.concatenate([x, random_state.randn(n_samples, 200 * n_features)], axis=1)
    # 针对二分类下的pr曲线
    x_train, x_test, y_train, y_test = train_test_split(x[y < 2], y[y < 2], test_size=0.5, random_state=random_state)
    return x_train, x_test, y_train, y_test


if __name__ == '__main__':
    x_train, x_test, y_train, y_test = get_dataset()
    model = LogisticRegression()
    model.fit(x_train, y_train)
    y_scores = model.predict_proba(x_test)
    precision, recall, _ = p_r_curve(y_test, y_scores[:, 1])
    ap = compute_ap(recall, precision)
    plt.plot(recall, precision, drawstyle="steps-post", label=f'LogisticRegression (AP={ap})')
    plt.legend(loc="lower left")
    plt.xlabel("Recall (Positive label: 1)")
    plt.ylabel("Precision (Positive label: 1)")
    # 通过sklear方法进行绘制
    plot_precision_recall_curve(model, x_test, y_test)
    plt.show()
