#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from multiset import Multiset
from multiprocessing.pool import Pool


modes = ['jaccard']


def jaccard(m, n):
	return len(m.intersection(n)) / len(m.union(n))


def pull(path):
	if not path:
		raise ValueError

	m = Multiset()
	with open(path) as f:
		for line in f:
			m.update(set(line.split(' ')))
	
	return m


@click.command()
@click.argument('first', type=click.Path())
@click.argument('second', type=click.Path())
@click.option('-m', 'mode', type=click.Choice(modes), default='jaccard')
def verify(first, second, mode):
	with Pool(2) as p:
		sets = tuple(p.map(pull, [first, second]))
	
	if mode == 'jaccard':
		similarity = jaccard(sets[0], sets[1])
	else:
		similarity = jaccard(sets[0], sets[1])
	
	click.echo('File {} and file {} have \'{}\' similarity.'.format(first, second, similarity))

if __name__ == '__main__':
	verify()
