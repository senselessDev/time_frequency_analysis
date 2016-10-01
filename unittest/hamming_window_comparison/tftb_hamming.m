close all;
clear all;

addpath('../tftb-source');

result = tftb_window(257, 'Hamming');

result_file = 'octave_hamming.csv';

save(result_file, 'result');
