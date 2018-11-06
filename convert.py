#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import sys


UP = (0, 101.54867260, 252.74336283)


def parse_args():
	args = sys.argv[1:]
	if len(args) != 2:
		sys.stderr.write('Usage: convert.py [origin] [target]\n')
		sys.exit(1)
	return args[0], args[1]


def mix(src, white):
	ret = [0, 0, 0]
	for i in range(3):
		alpha = (255 - white[i]) / (255 - UP[i])
		dst = UP[i] * alpha + src[i] * (1 - alpha)
		ret[i] = max(0, min(255, int(dst)))
	return tuple(ret)


def reserve_rgb(dst, white):
	#      dst = up * alpha + dw * (1 - alpha)
	# => alpha = (dst - dw) / (up - dw)
	ret = [0, 0, 0]
	for i in range(3):
		alpha = (255 - white[i]) / (255 - UP[i])
		down = (dst[i] - UP[i] * alpha) / (1 - alpha)
		ret[i] = int(down)
	return tuple(ret)


def reverse(img, white):
	width, height = white.size
	_, ih = img.size
	white = white.load()
	pixels = img.load()

	for x in range(width):
		for y in range(height):
			nxy = (x, ih - height + y)
			result = reserve_rgb(pixels[nxy], white[x, y])
			pixels[nxy] = result

	return img


def check_distance(result, white, img):
	difference = 0

	width, height = white.size
	_, ih = img.size
	white = white.load()
	pixels = result.load()
	std = img.load()

	for x in range(width):
		for y in range(height):
			nxy = (x, ih - height + y)
			origin = std[nxy]
			target = mix(pixels[nxy], white[x, y])
			difference += sum([abs(a - b) for (a, b) in zip(target, origin)]) ** 2

	return difference


def main():
	origin, target = parse_args()
	white = Image.open('base.png')
	img = Image.open(origin)
	result = reverse(img, white)
	diff = check_distance(result, white, Image.open(origin))
	sys.stdout.write('Difference: {}\n'.format(round(diff / 1000000, 8)))
	result.save(target)


if __name__ == '__main__':
	main()
