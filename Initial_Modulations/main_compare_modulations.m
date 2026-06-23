clear; clc; close all;

% Recursively add all subfolders in the current directory
addpath(genpath(pwd));

% Creates a configuration structure (cfg)
cfg.seed          = 42;
cfg.numBits       = 2e6;      % keep divisible by 2, 3, 4, 6 if possible
cfg.EbNoVec       = 0:1:15;
cfg.plotEbNo      = 6;        % noisy constellation snapshot
cfg.showClean     = true;
cfg.showNoisy     = true;

% Initialize random number generator (rng) using the Mersenne Twister algo
rng(cfg.seed, 'twister');

specs = [
    struct('name', "BPSK",   'type', "psk",    'M', 2,  'phaseOffset', 0)
    struct('name', "QPSK",   'type', "psk",    'M', 4,  'phaseOffset', pi/4)
    struct('name', "8-PSK",  'type', "psk",    'M', 8,  'phaseOffset', pi/8)
    struct('name', "8-QAM",  'type', "genqam", 'M', 8,  'phaseOffset', 0)
    struct('name', "16-QAM", 'type', "qam",    'M', 16, 'phaseOffset', 0)
    struct('name', "64-QAM", 'type', "qam",    'M', 64, 'phaseOffset', 0)
];

% Preallocate a cell array to store the simulation results for each scheme
results = cell(numel(specs), 1);    % dimension: len(specs) x 1

% Loops through each defined modulation scheme
for i = 1:numel(specs)
    fprintf('Running %s...\n', specs(i).name);
    results{i} = run_modulation_case(specs(i), cfg);

    if cfg.showClean
        figure('Name', specs(i).name + " Clean Constellation");
        plot_constellation(results{i}.txSig, specs(i).name + " (No Noise)", results{i}.refConstellation);
    end

    if cfg.showNoisy && ~isempty(results{i}.rxSigPlot)
        figure('Name', specs(i).name + " Noisy Constellation");
        plot_constellation(results{i}.rxSigPlot, ...
            specs(i).name + " - AWGN at " + string(cfg.plotEbNo) + " dB", ...
            results{i}.refConstellation);
    end
end

figure('Name', 'BER Comparison');
plot_ber_curve(cfg.EbNoVec, results);

save('results/phase_1_results.mat', 'cfg', 'specs', 'results');
disp('Done. Saved to phase1_results.mat');