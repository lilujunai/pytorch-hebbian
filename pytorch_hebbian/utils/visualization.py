import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


def show_image(image, title=None):
    np_img = image.numpy()
    plt.imshow(np.transpose(np_img, (1, 2, 0)))
    if title is not None:
        plt.title(title)
    plt.show()


def draw_synapse(synapse, shape):
    mat = np.reshape(synapse, shape)
    im = plt.matshow(mat, cmap='bwr', interpolation='nearest')
    plt.colorbar(im, ticks=[np.amin(mat), 0, np.amax(mat)])
    plt.show()


def draw_weights(synapses, shape, height, width):
    if len(shape) == 1:
        dim = int(np.sqrt(int(shape[0])))
        shape = (dim, dim)

    fig, axs = plt.subplots(height, width,
                            sharex='col',
                            sharey='row',
                            gridspec_kw={'hspace': 0, 'wspace': 0})
    fig.suptitle('Weights')

    mats = []
    index = 0
    for i in range(height):
        for j in range(width):
            synapse = synapses[index]
            index += 1
            mat = np.reshape(synapse, shape)
            mats.append(axs[i, j].matshow(mat, cmap='bwr'))

    for ax in fig.get_axes():
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(bottom=False, top=False, labelbottom=False)

    # Find the min and max of all colors for use in setting the color scale.
    images = mats
    vmin = min(image.get_array().min() for image in images)
    vmax = max(image.get_array().max() for image in images)
    norm = colors.Normalize(vmin=-vmax, vmax=vmax)
    for im in images:
        im.set_norm(norm)

    fig.colorbar(images[0],
                 ax=axs,
                 orientation='horizontal',
                 fraction=.1,
                 ticks=[vmin, 0, vmax])
    plt.show()


def weights_to_grid(weights, input_shape):
    # If no height or width is specified create the smallest fitting square grid
    num_weights = weights.shape[0]
    height = width = math.ceil(math.sqrt(num_weights))

    # Put all perceptrons in a single array
    dim_y, dim_x, depth = input_shape
    data = np.zeros((dim_y * height, dim_x * width, depth))

    yy = 0
    for y in range(height):
        for x in range(width):
            if yy < num_weights:
                perceptron = weights[yy].reshape((depth, dim_y, dim_x)).transpose((1, 2, 0))
                data[y * dim_y:(y + 1) * dim_y, x * dim_x:(x + 1) * dim_x, :] = perceptron
                yy += 1
            else:
                break

    return data


def plot_learning_curve(train_losses, val_losses, epochs=None):
    if epochs is None:
        epochs = list(range(len(train_losses)))

    plt.plot(epochs, train_losses, label='Train loss')
    plt.plot(epochs, val_losses, label='Validation loss')
    plt.title('Learning curves')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend()
    plt.show()


def plot_accuracy(accuracies, epochs=None):
    if epochs is None:
        epochs = list(range(len(accuracies)))

    plt.plot(epochs, accuracies, label='Validation accuracy')
    plt.title('Accuracy curve')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend()
    plt.show()