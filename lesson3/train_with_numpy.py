# 引入包
import matplotlib.pyplot as plt
import numpy as np

from IPython import display

import utils


def load_data():
    """
    载入数据,包括训练和测试数据
    Args:
    Return:
        X_train：训练数据集
        Y_train：训练数据标签
        X_test：测试数据集
        Y_test：测试数据标签
        classes(cat/non-cat)：分类list
        px_num:数据的像素长度
    """
    # 调用utils.load_data_sets()方法，获取数据
    X_train, Y_train, X_test, Y_test, classes = utils.load_data_sets()

    # 获取数据相关信息
    train_num = X_train.shape[0]    # train_num: 训练集中样本数量
    test_num = X_test.shape[0]      # test_num: 测试集中样本数量
    px_num = X_train.shape[1]       # px_num: 每张图片的长度，单位为像素

    # 转换数据形状
    data_dim = px_num * px_num * 3
    X_train = X_train.reshape(train_num, data_dim).T
    X_test = X_test.reshape(test_num, data_dim).T

    # 数据归一化处理
    X_train = X_train / 255.
    X_test = X_test / 255.

    data = [X_train, Y_train, X_test, Y_test, classes, px_num]

    return data


def sigmoid(x):
    """
    定义sigmoid激活函数
    """
    return 1 / (1 + np.exp(-x))


def initialize_parameters(data_dim):
    """
    参数W和b初始化为0
    Args:
        data_dim: W向量的纬度
    Returns:
        W: (dim, 1)维向量
        b: 标量，代表偏置bias
    """
    W = np.zeros((data_dim, 1), dtype=np.float)
    b = 0.0

    return W, b


def forward_and_backward_propagate(X, Y, W, b):
    """
    计算成本Cost和梯度grads
    Args:
        W: 权重， (num_px * num_px * 3, 1)维的numpy数组
        b: 偏置bias
        X: 数据，shape为(num_px * num_px * 3, number of examples)
        Y: 数据的标签( 0 if non-cat, 1 if cat) ，shape (1, number of examples)
    Return:
        cost: 逻辑回归的损失函数
        dW: cost对参数W的梯度，形状与参数W一致
        db: cost对参数b的梯度，形状与参数b一致
    """
    m = X.shape[1]

    # 前向传播，计算成本函数
    Z = np.dot(W.T, X) + b
    A = sigmoid(Z)
    dZ = A - Y

    cost = np.sum(-(Y * np.log(A) + (1 - Y) * np.log(1 - A))) / m

    # 后向传播，计算梯度
    dW = np.dot(X, dZ.T) / m
    db = np.sum(dZ) / m

    cost = np.squeeze(cost)

    grads = {
        "dW": dW,
        "db": db
    }

    return grads, cost


def update_parameters(X, Y, W, b, learning_rate):
    """
    更新参数
    Args:
        X: 整理后的输入数据
        Y: 标签
        W: 参数W
        b: bias
        learning_rate: 学习步长
    Return：
        W：更新后的参数W
        b：更新后的bias
        cost：成本
    """
    grads, cost = forward_and_backward_propagate(X, Y, W, b)

    W = W - learning_rate * grads['dW']
    b = b - learning_rate * grads['db']

    return W, b, cost


def train(X, Y, W, b, iteration_nums, learning_rate):
    """
    训练的主过程，使用梯度下降算法优化参数W和b
    Args:
        X: 数据，shape为(num_px * num_px * 3, number of examples)
        Y: 数据的标签(0 if non-cat, 1 if cat) ，shape为 (1, number of examples)
        W: 权重， (num_px * num_px * 3, 1)维的numpy数组
        b: 偏置bias，标量
        iteration_nums: 训练的迭代次数
        learning_rate: 梯度下降的学习率，可控制收敛速度和效果
    Returns:
        params: 包含参数W和b的python字典
        costs: 保存了优化过程cost的list，可以用于输出cost变化曲线
    """
    costs = []
    for i in range(iteration_nums):
        W, b, cost = update_parameters(X, Y, W, b, learning_rate)

        if i % 100 == 0:
            costs.append(cost)
            draw(costs)
            print("Iteration %d, cost %f" % (i, cost))

    params = {
        "W": W,
        "b": b
    }

    return params, costs


def predict_image(X, W, b):
    """
    用学习到的逻辑回归模型来预测图片是否为猫（1 cat or 0 non-cat）
    Args:
        X: 数据，形状为(num_px * num_px * 3, number of examples)
        W: 权重， (num_px * num_px * 3, 1)维的numpy数组
        b: 偏置bias
    Returns:
        predictions: 包含了对X数据集的所有预测结果，是一个numpy数组或向量
    """
    data_dim = X.shape[0]

    m = X.shape[1]

    predictions = []

    W = W.reshape(data_dim, 1)

    # 预测概率结果为A
    A = sigmoid(np.dot(W.T, X) + b)

    # 将连续值A转化为二分类结果0或1
    # 阈值设定为0.5即预测概率大于0.5则预测结果为1
    for i in range(m):
        if A[0, i] >= 0.5:
            predictions.append(1)
        elif A[0, i] < 0.5:
            predictions.append(0)

    return predictions


def calc_accuracy(predictions, Y):
    """
    计算train准确度
    """
    Y = np.squeeze(Y)
    right = 0
    for i in range(len(predictions)):
        if predictions[i] == Y[i]:
            right += 1
    accuracy = (right / float(len(predictions))) * 100
    return accuracy


def plot_costs(costs, learning_rate):
    """
    利用costs展示模型的学习曲线
    """
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('Iterations (per hundreds)')
    plt.title("learning rate =" + str(learning_rate))
    plt.show()
    plt.savefig('costs.png')


def draw_line(costs):
    plt.title("train cost")
    plt.clf()
    plt.plot(costs)
    plt.pause(0.01)
    display.clear_output(wait=True)


def draw(costs):
    plt.figure("draw costs")
    draw_line(costs)


def main():
    """
    main entry
    """
    plt.ion()
    # 获取数据
    X_train, Y_train, X_test, Y_test, classes, px_num = load_data()

    # 设置迭代次数
    iteration_nums = 2000

    # 设置学习率
    learning_rate = 0.005

    # 设置特征维度
    data_dim = X_train.shape[0]

    # 初始化参数
    W, b = initialize_parameters(data_dim)

    # 训练
    params, costs = train(X_train, Y_train, W, b, iteration_nums, learning_rate)

    predictions_train = predict_image(X_train, params['W'], params['b'])
    predictions_test = predict_image(X_test, params['W'], params['b'])

    print("Accuracy on train set: {} %".format(calc_accuracy(predictions_train, Y_train)))
    print("Accuracy on test set: {} %".format(calc_accuracy(predictions_test, Y_test)))

    # 预测示例
    index = 1  # index(1) is a cat, index(14) not a cat
    cat_img = X_test[:, index].reshape((px_num, px_num, 3))

    # 设置绘图窗口
    plt.figure("results")
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    plt.sca(ax1)
    plt.title("the %d's picture" % (index))
    plt.imshow(cat_img)
    plt.axis('off')
    plt.show()
    print(
        "The label of this picture is " + str(Y_test[0, index])
        + ", 1 means it's a cat picture, 0 means not "
        + "\nYou predict that it's a "
        + classes[int(predictions_test[index])].decode("utf-8")
        + " picture. \nCongrats!"
    )

    # 绘制学习曲线
    plt.sca(ax2)
    plot_costs(costs, learning_rate)


if __name__ == "__main__":
    main()