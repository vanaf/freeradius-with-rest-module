# Makefile for source rpm: freeradius
# $Id$
NAME := freeradius
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
