# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 18:14:10 2018

@author: Akhil
"""

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import img_as_float
from mpl_toolkits.mplot3d import Axes3D
import sys


def k_means_clustering(img_vect, k, numiter):
    clus_ptypes = np.random.rand(k, 3)
    lbls = np.full((img_vect.shape[0],), -1)
    for i in range(numiter):
        print('Iteration number : ' + str(i + 1))
        points_lbl = [None for x in range(k)]
        for iter_i, j in enumerate(img_vect):
            color_rows = np.repeat(j, k).reshape(3, k).T
            near_label = np.argmin(np.linalg.norm(color_rows - clus_ptypes, axis=1))
            lbls[iter_i] = near_label
            if points_lbl[near_label] is None:
                points_lbl[near_label] = []
            points_lbl[near_label].append(j)
        for x in range(k):
            if (points_lbl[x] is not None):
                length1 = len(points_lbl[x])
                new_cluster_prototype = np.asarray(points_lbl[x]).sum(axis=0) / length1
                clus_ptypes[x] = new_cluster_prototype

    return (lbls, clus_ptypes)

def plot_image_colors_by_label(name, img_vect, lbls, clus_ptypes):
    image1 = plt.figure()
    axes = Axes3D(image1)
    for x, y in enumerate(img_vect):
        axes.scatter(y[0], y[1], y[2], c=clus_ptypes[lbls[x]], marker='o')
    axes.set_ylabel('Green')
    axes.set_xlabel('Red')
    axes.set_zlabel('Blue')
    image1.savefig(name + '.png')


def plot_image_colors_by_color(name, img_vect):
    image2 = plt.figure()
    axes1 = Axes3D(image2)

    for x in img_vect:
        axes1.scatter(x[0], x[1], x[2], c=x, marker='o')
    axes1.set_zlabel('Blue')
    axes1.set_xlabel('Red')
    axes1.set_ylabel('Green')
    image2.savefig(name + '.png')

if __name__ == '__main__':
    
    img = sys.argv[1]
    image11 = sys.argv[1]
    K= int(sys.argv[2])
    itr= int(sys.argv[3])
    img = io.imread(img)[:, :, :3] 
    img = img_as_float(img)

    image_dimensions = img.shape
    image_name = img
    img_vect = img.reshape(-1, img.shape[-1])
    lbls, color_centroids = k_means_clustering(img_vect, k=K, numiter=itr)
    out_img = np.zeros(img_vect.shape)
    for i in range(out_img.shape[0]):
        out_img[i] = color_centroids[lbls[i]]
    out_img = out_img.reshape(image_dimensions)
    print('Saving Compressed Image...')
    if K==2:
        if image11 == 'Koala.jpg':
            io.imsave('k2.jpg' , out_img)
        if image11 == 'Penguins.jpg':
            io.imsave('p2.jpg' , out_img)
    elif K==5:
        if image11 == 'Koala.jpg':
            io.imsave('k5.jpg' , out_img)
        if image11 == 'Penguins.jpg':
            io.imsave('p5.jpg' , out_img)
    elif K==10:
        if image11 == 'Koala.jpg':
            io.imsave('k10.jpg' , out_img)
        if image11 == 'Penguins.jpg':
            io.imsave('p10.jpg' , out_img)
    elif K==15:
        if image11 == 'Koala.jpg':
            io.imsave('k15.jpg' , out_img)
        if image11 == 'Penguins.jpg':
            io.imsave('p15.jpg' , out_img)
    elif K==20:
        if image11 == 'Koala.jpg':
            io.imsave('k20.jpg' , out_img)
        if image11 == 'Penguins.jpg':
            io.imsave('p20.jpg' , out_img)
    else:
        io.imsave('compressedimage.jpg', out_img)
    print('Image compressed successfully!')