// Copyright (c) 2024 dongdongcan
// This code is licensed under the Apache License.
// See the LICENSE file for details.

#pragma once

float* my_conv2d(float* img,
                 float* weight,
                 int hi,
                 int wi,
                 int& ho,
                 int& wo,
                 int ci,
                 int co,
                 int kernel,
                 int stride,
                 int pad,
                 bool is_first,
                 bool is_free_img = true);
