// Copyright (c) 2024 dongdongcan
// This code is licensed under the Apache License.
// See the LICENSE file for details.

#pragma once
#include <immintrin.h>

#include <cmath>
#include <cstdint>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>

float* MyMaxPoolPreLoad(float* img);

float* MyMaxPool(float* img);

float* MyAvgPoolPreLoad(float* img);

float* MyAvgPool(float* img);
