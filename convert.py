#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import sys


white = None
black = None


def parse_args():
	args = sys.argv[1:]
	if len(args) != 2:
		sys.stderr.write('Usage: convert.py [origin] [target]\n')
		sys.exit(1)
	return args[0], args[1]


def mix(down, up, alpha):
	return tuple([int(up[i] * alpha + down[i] * (1 - alpha)) for i in range(3)])


def get_override_rgb(white, black):
	ret = [0, 0, 0]
	for i in range(3):
		alpha = 1 - (white[i] - black[i]) / 255
		ret[i] = int(black[i] / alpha) if alpha != 0 else None
	return tuple(ret)


def reverse_rgb(target, white, black):
	"""Reverse a rgb pixel

	Mix formula: dst = up * alpha + dw * (1 - alpha)
	             dst = (up - dw) * alpha + dw

	Get `alpha` and `up`:
		1. dst_b = (up - dw_b) * alpha + dw_b     (Black, dst_b = `black`)
		2. dst_w = (up - dw_w) * alpha + dw_w     (White, dst_w = `white`)

		alpha = 1 - (dst_b - dst_w) / (dw_b - dw_w)
		   up = (dst_b + dw_b * (alpha - 1)) / alpha

		Code:
		``` python
		alpha = 1 - (white[i] - black[i]) / 255
		up = black[i] / alpha
		```

	Get `down`:
		  dst = up * alpha + dw * (1 - alpha)     (dst = `target`)
		=> dw = (dst - up * alpha) / (1 - alpha)

		Code: `down = (target[i] - up * alpha) / (1 - alpha)`
	"""
	ret = [0, 0, 0]
	for i in range(3):
		alpha = 1 - (white[i] - black[i]) / 255
		if alpha == 0:
			ret[i] = target[i]
		else:
			up = black[i] / alpha
			down = (target[i] - up * alpha) / (1 - alpha)
			ret[i] = int(down)
	return tuple(ret)


def reverse(img):
	global white, black

	width, height = white.size
	_, ih = img.size
	white_pixel = white.load()
	black_pixel = black.load()
	pixels = img.load()

	for x in range(width):
		for y in range(height):
			nxy = (x, ih - height + y)
			result = reverse_rgb(pixels[nxy], white_pixel[x, y], black_pixel[x, y])
			pixels[nxy] = result

	return img


def check_distance(result, img):
	global white, black

	difference = 0

	width, height = white.size
	_, ih = img.size
	white_pixel = white.load()
	black_pixel = black.load()
	pixels = result.load()
	std = img.load()

	for x in range(width):
		for y in range(height):
			nxy = (x, ih - height + y)
			up = get_override_rgb(white_pixel[x, y], black_pixel[x, y])
			if any((item is not None for item in up)):
				origin = std[nxy]
				target = mix(pixels[nxy], up, 0.5)
				difference += sum([abs(a - b) for (a, b) in zip(target, origin)]) ** 2

	return difference


def main():
	global white, black
	white = Image.open('base_white.png')
	black = Image.open('base_black.png')

	origin, target = parse_args()
	img = Image.open(origin)
	result = reverse(img)
	result.save(target)

	diff = check_distance(result, Image.open(origin))
	sys.stdout.write('Difference: {}\n'.format(round(diff / 1000000, 8)))


if __name__ == '__main__':
	main()
