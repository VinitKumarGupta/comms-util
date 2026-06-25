function result = run_modulation_case(spec, cfg)
%RUN_MODULATION_CASE  Simulate one modulation scheme across Eb/N0 values.

bitsIn = randi([0 1], cfg.numBits, 1); % a column vector of random 0s and 1s
k = log2(spec.M);   % Calculates the number of bits per symbol

% Call the modulation function
[txSig, txBitsPadded, padBits, txSym, refConst] = modulate_signal(bitsIn, spec);

% Clean channel
[rxBitsClean, rxSymClean] = demodulate_signal(txSig, spec);
numOrigBits = numel(bitsIn);

% Calculates BER on the clean signal (should be 0)
[berClean, errClean] = compute_ber(bitsIn, rxBitsClean(1:numOrigBits));

% Preallocates arrays to store BER results for each Eb/N0 step
berSim   = zeros(numel(cfg.EbNoVec), 1);
errCount  = zeros(numel(cfg.EbNoVec), 1);
rxSigPlot = [];
rxBitsPlot = [];
rxSymPlot  = [];

% Sweeps through the defined signal-to-noise ratios
for ii = 1:numel(cfg.EbNoVec)
    EbNo = cfg.EbNoVec(ii); % Extract the current Eb/N0 value

    % Add the calculated noise to the transmitted signal
    [rxSig, noiseVar, snrDb] = add_awgn_noise(txSig, EbNo, k);

    % Demodulate the noisy signal
    [rxBits, rxSym] = demodulate_signal(rxSig, spec);

    % Calculates and stores the BER
    [berSim(ii), errCount(ii)] = compute_ber(bitsIn, rxBits(1:numOrigBits));

    if abs(EbNo - cfg.plotEbNo) < 1e-12
        rxSigPlot = rxSig;
        rxBitsPlot = rxBits;
        rxSymPlot  = rxSym;
    end
end

% Theoretical BER (only for standard PSK/QAM cases) using built-in func
berTheory = nan(numel(cfg.EbNoVec), 1);
if spec.type == "psk"
    berTheory = berawgn(cfg.EbNoVec(:), 'psk', spec.M, 'nondiff');
elseif spec.type == "qam"
    berTheory = berawgn(cfg.EbNoVec(:), 'qam', spec.M);
end

result = struct();
result.name           = spec.name;
result.type           = spec.type;
result.M              = spec.M;
result.bitsPerSymbol   = k;
result.bitsIn         = bitsIn;
result.txSig          = txSig;
result.txSym          = txSym;
result.txBitsPadded   = txBitsPadded;
result.padBits        = padBits;
result.refConstellation = refConst;
result.rxSigPlot      = rxSigPlot;
result.rxBitsPlot     = rxBitsPlot;
result.rxSymPlot      = rxSymPlot;
result.berClean       = berClean;
result.errClean       = errClean;
result.berSim         = berSim;
result.errCount       = errCount;
result.berTheory      = berTheory;
end