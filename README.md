﻿# Zero Pairs Machine

See it in action here: https://youtu.be/vuKl-nOsUQk

This repository contains the code for building a servo-powered model that visually demonstrates the concept of zero pairs, making it easier to understand how to add and subtract negative numbers.

## Features

Uses a Raspberry Pi to control servo motors, which move spheres representing positive and negative units.
A Flask web interface allows users to input numbers and operations directly from a browser.
Visually demonstrates zero pair cancellation and the resulting answers to addition and subtraction problems involving negative numbers.

## How it Works

The model uses two types of spheres:

- White/Black spheres represent positive units.
- Orange/Black spheres represent negative units.

The servos move the spheres to form zero pairs, which then cancel each other out, leaving the remaining units to represent the answer to the calculation.
