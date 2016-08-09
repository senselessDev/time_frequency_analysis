close all;
clear all;

addpath('tftb-source');

sz = 1025;
x = 0:sz-1;
y=sin(2*pi*(0.02 + 0.04 / sz * x).*x);
[tfr, t, f] = tfrspwv(y');

result_file = "octave_spwvd.csv";

save(result_file, "tfr")
disp([pwd(), "/", result_file])
