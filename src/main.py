#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Torrez, Milton N.

from scripts.meteorologia_paraguay import meteorlogia_py_main


if __name__ == "__main__":

    try:
        meteorlogia_py_main()

    except Exception as e:
        print(e)
