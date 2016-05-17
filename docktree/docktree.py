# -*- coding: utf-8 -*-

"""
Analyse dependencies of docker images.
"""

from __future__ import absolute_import
from .ImageLayer import ImageLayer

import docker
import copy


def _fetch_all_layers():
    """:return: a list of all image layers as dict generated by docker api"""
    docker_cli = docker.Client()
    return docker_cli.images(all=True)


def analyze_layers(images=None):
    """
    analyze all layers and compute a tree
    :param images: list of dicts of images provided by docker api (optional)
    :return: dict of images. Key is identifier, value is instance of ImageLayer
    :rtype: dict
    """

    if not images:
        images = _fetch_all_layers()
    layers = {}

    for image in images:
        layer = ImageLayer(
            identifier=image['Id'],
            tags=[tag for tag in image['RepoTags'] if tag != '<none>:<none>'],
            size=image['VirtualSize'],
        )
        layers[image['Id']] = layer

    for image in images:
        if image['ParentId'] != '':
            ImageLayer.join_parent_child(
                parent=layers[image['ParentId']],
                child=layers[image['Id']],
            )

    return layers


def get_heads(layers, for_image=None):
    """
    return the head(s) of the specified image or all heads of a given tree
    :param layers: double linked list of layers
    :param for_image: image to get heads for
    :return: heads of the specified image or all heads of a given tree
    :rtype: list
    """
    if not for_image:
        return [layer for layer in layers.values() if layer.is_head()]

    heads = []

    for layer_id, layer in layers.items():
        if not layer_id.startswith(for_image) and \
                not [t for t in layer.tags if t.startswith(for_image)]:
            continue

        next_parent = layer.parent
        if next_parent is None:
            heads.append(layer)
            continue
        while not next_parent.is_head():
            next_parent = next_parent.parent
        heads.append(next_parent)

    return heads


def remove_untagged_layers(layers):
    """
    deepcopy the layers dict and remove all untagged layers from the tree
    :param layers: dict containing all layers
    :return: tree without untagged layers
    :rtype: dict
    """
    layers_cpy = copy.deepcopy(layers)
    layer_ids_to_remove = []
    for layer_id, layer in layers_cpy.items():
        if not layer.tags:
            layer.remove_from_chain()
            layer_ids_to_remove.append(layer_id)

    for layer_id in layer_ids_to_remove:
        layers_cpy.pop(layer_id)
    return layers_cpy
