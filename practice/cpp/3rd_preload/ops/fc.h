// Copyright (c) 2024 dongdongcan
// This code is licensed under the MIT License.
// See the LICENSE file for details.

#pragma once
#include <immintrin.h>

#include <cmath>
#include <cstdint>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>

float* MyFCPreLoad(float* img, float* weight, float* bias);

float* MyFC(float* img, float* weight, float* bias);
