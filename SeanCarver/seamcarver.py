from pylab import imread
from pylab import inf
from pylab import figure
from pylab import subplot
from pylab import title
from pylab import imshow
from pylab import show
from pylab import gray
from skimage import img_as_float
from skimage import filters
import numpy


def dual_gradient_energy(img):
    """
    This method will calculate the dual gradient energy for a given image.
    The energy is the sum of the squares of the horizontal and
    vertical gradients.

    Testing the dual gradient energy values for a sample output
    >>> from pylab import array
    >>> def test():
    ...     img = array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]])
    ...     return dual_gradient_energy(img)
    >>> test()
    array([[ 0.,  0.],
           [ 0.,  0.]])
    """
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    horizontal_red = filters.sobel_h(R)
    horizontal_green = filters.sobel_h(G)
    horizontal_blue = filters.sobel_h(B)

    vertical_red = filters.sobel_v(R)
    vertical_green = filters.sobel_v(G)
    vertical_blue = filters.sobel_v(B)

    horizontal_square_sum = add_squares(horizontal_red,
                                        horizontal_green, horizontal_blue)

    vertical_square_sum = add_squares(vertical_red,
                                      vertical_green, vertical_blue)

    energy = numpy.add(horizontal_square_sum, vertical_square_sum)

    return energy


def add_squares(a, b, c):
    """
    This method is used to add the squares of the given 3 values.
    """
    return numpy.add(numpy.square(a), numpy.add(numpy.square(b),
                                                numpy.square(c)))


def find_seam(img):
    """
    This method will calculate the seam path that is to be
    removed from the image.

    Testing if the first 10 seam values are correct
    >>> def test():
    ...     img = imread("image-slider-2.jpg")
    ...     img_seam_carved = img_as_float(img)
    ...     energy = dual_gradient_energy(img_seam_carved)
    ...     seam = find_seam(energy)
    ...     return seam[0:10]
    >>> test()
    [685.0, 685.0, 684.0, 683.0, 684.0, 685.0, 684.0, 683.0, 682.0, 681.0]
    """
    rows = img.shape[0]
    cols = img.shape[1]

    # seam_path_mapper will hold all the minimum paths from each index in a row
    # That is, this mapper will contain information whether the next path from
    # the current index is left, straight or right
    seam_path_mapper = numpy.zeros(shape=(rows, cols))

    # img_energy will contain the aggregate energies for all paths
    img_energy = numpy.zeros(shape=(rows, cols))

    """
    The below logic will find the least energy value among
    left, center and right values from the previous row for
    each column in each row.
    img_list will contain left, center and right img energy
    values for each index in a row.
    energy_list will contain the weighted values of energies.
    """
    for i in range(1, rows):
        for j in range(1, cols - 1):

            if j == 1:
                img_list = [inf, img[i - 1][j], img[i - 1][j + 1]]
                energy_list = [inf, img_energy[i - 1][j],
                               img_energy[i - 1][j + 1]]
            elif j == (cols - 2):
                img_list = [img[i - 1][j - 1], img[i - 1][j], inf]
                energy_list = [img_energy[i - 1][j - 1],
                               img_energy[i - 1][j], inf]
            else:
                img_list = [img[i - 1][j - 1], img[i - 1][j],
                            img[i - 1][j + 1]]
                energy_list = [img_energy[i - 1][j - 1], img_energy[i - 1][j],
                               img_energy[i - 1][j + 1]]

            if i == 1:
                img_energy[i][j] = img[i][j]
                seam_path_mapper[i][j] = j
            else:
                min_index = img_list.index(min(img_list))
                minimum = energy_list[min_index]

                img_energy[i][j] = img[i][j] + minimum
                if min_index == 0:
                    seam_path_mapper[i][j] = j - 1
                elif min_index == 1:
                    seam_path_mapper[i][j] = j
                elif min_index == 2:
                    seam_path_mapper[i][j] = j + 1

    return calculate_seam(rows, cols, img_energy, seam_path_mapper)


def calculate_seam(rows, cols, img_energy, seam_path_mapper):
    """
    This method will calculate the seam indexes for each row
    """

    # seam will hold the indexes of the seam points in each row.
    seam = []
    index = 0

    # Calculating the minimum index for the last row
    min_val = inf
    for i in range(1, cols - 1):
        cur_val = img_energy[rows - 1][i]
        if cur_val < min_val:
            min_val = cur_val
            index = i

    seam.insert(0, index)
    index = seam_path_mapper[rows - 1][index]

    # Plotting the seam path from last row moving upwards
    for i in range(rows - 2, -1, -1):
        seam.insert(0, index)
        index = seam_path_mapper[i][index]

    return seam


def plot_seam(img, seam):
    """
    This method is used to display seam points on the image.

    We are testing if the seam point has been plotted in the
    0th row of the image
    >>> def test():
    ...     img = imread("image-slider-2.jpg")
    ...     img_seam_plot = img_as_float(img)
    ...
    ...     energy = dual_gradient_energy(img_seam_plot)
    ...     seam = find_seam(energy)
    ...     img_seam_plot = plot_seam(img_seam_plot, seam)
    ...     return img_seam_plot[0][seam[0]]
    >>> test()
    array([ 1.,  0.,  0.])
    """
    point = [1, 0, 0]
    rows = img.shape[0]

    for i in range(0, rows):
        img[i][seam[i]] = point

    return img


def remove_seam(img, seam):
    """
    This method is used to remove the seam from the image.

    In the test below showing one seam is removed
    >>> def test():
    ...     img = imread("image-slider-2.jpg")
    ...     img_seam_carved = img_as_float(img)
    ...     img_original = img_as_float(img)
    ...     energy = dual_gradient_energy(img_seam_carved)
    ...     seam = find_seam(energy)
    ...     img_seam_carved = remove_seam(img_seam_carved, seam)
    ...     return img_seam_carved.shape[1], img_original.shape[1]
    >>> test()
    (699L, 700L)
    """
    seam_rows = len(seam)
    for i in range(0, seam_rows):
        # Finding the seam point in a row,
        # moving all the values in the row before the seam point to
        # the right by one index,
        # deleting the first column from the row
        seam_col = seam[i]
        img[i, 1:seam_col + 1, :] = img[i, 0:seam_col, :]

    return numpy.delete(img, 0, 1)


def main():
    """
    Testing to see if the image is carved.
    That is, we are removing 2 seams from the image and checking
    if the column size has been decreased
    >>> def test():
    ...     img = imread("image-slider-2.jpg")
    ...     img_original = img_as_float(img)
    ...     img_seam_carved = img_as_float(img)
    ...     for i in range(0, 2):
    ...         energy = dual_gradient_energy(img_seam_carved)
    ...         seam = find_seam(energy)
    ...         img_seam_carved = remove_seam(img_seam_carved, seam)
    ...     return img_seam_carved.shape[1], img_original.shape[1]
    >>> test()
    (698L, 700L)
    """

    img = imread("image-slider-2.jpg")
    img_seam_plot = img_as_float(img)
    img_original = img_as_float(img)
    img_seam_carved = img_as_float(img)

    img_seam_horizontal = img_as_float(img).transpose(1, 0, 2)
    img_seam_carved_horizontal = img_as_float(img).transpose(1, 0, 2)

    figure()
    gray()
    subplot(3, 2, 1)
    imshow(img_original)
    title("Original")

    # Removing 50 seams
    for i in range(0, 50):
        energy = dual_gradient_energy(img_seam_carved)
        seam = find_seam(energy)

        img_seam_plot = plot_seam(img_seam_plot, seam)
        img_seam_carved = remove_seam(img_seam_carved, seam)

        energy_horizontal = dual_gradient_energy(img_seam_carved_horizontal)
        seam_horizontal = find_seam(energy_horizontal)

        img_seam_horizontal = plot_seam(img_seam_horizontal, seam_horizontal)
        img_seam_carved_horizontal = remove_seam(img_seam_carved_horizontal,
                                                 seam_horizontal)

    subplot(3, 2, 3)
    imshow(img_seam_plot)
    title("Vertical Seam Plot")

    subplot(3, 2, 5)
    imshow(img_seam_carved)
    title("Vertical Carved Image")

    subplot(3, 2, 4)
    imshow(img_seam_horizontal.transpose(1, 0, 2))
    title("Horizontal Seam Plot")

    subplot(3, 2, 6)
    imshow(img_seam_carved_horizontal.transpose(1, 0, 2))
    title("Horizontal Carved Image")

    show()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
