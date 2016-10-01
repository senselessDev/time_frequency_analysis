close all;
clear all;

addpath('tftb-source');

sz = 1024;
x = 0:sz-1;
y=sin(2*pi*(0.02 + 0.04 / sz * x).*x);
[tfr, t, f] = tfrwv(y');

result_file = "octave_wvd_even.csv";

save(result_file, "tfr")
disp([pwd(), "/", result_file])
