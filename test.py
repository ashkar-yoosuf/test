c#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 21:54:39 2018

@author: ashkar
"""
class Dog:

    # Class Attribute
    species = 'mammal'

    # Initializer / Instance Attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age


# Instantiate the Dog object
philo = Dog("Philo", 5)
mikey = Dog("Mikey", 6)

# Access the instance attributes
print("{} is {} and {} is {}.".format(
    philo.name, philo.age, mikey.name, mikey.age))

# Is Philo a mammal?
if philo.species == "mammal":
    print("{1} is a {0}!".format(philo.species, philo.name))