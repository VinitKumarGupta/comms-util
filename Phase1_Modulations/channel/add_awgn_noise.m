function [rxSig, noiseVar, snrDb] = add_awgn_noise(txSig, EbNoDb, bitsPerSymbol)
%ADD_AWGN_NOISE  Add complex AWGN from Eb/N0.

txSig = txSig(:);

% Calculates the average power of the transmitted complex signal
txPower = mean(abs(txSig).^2);

% Converts Energy per Bit (Eb/N0) to Signal-to-Noise Ratio (SNR) by 
% factoring in the spectral efficiency (bits per symbol)
snrDb = EbNoDb + 10*log10(bitsPerSymbol);

% Converts logarithmic dB into a linear scale
snrLin = 10^(snrDb/10);

% Determines the required noise variance based on the desired SNR
noiseVar = txPower / snrLin;

% Generates complex Gaussian noise. The variance is divided by 2 because 
% the noise power must be split equally between the real (In-Phase) and 
% imaginary (Quadrature) components
noise = sqrt(noiseVar/2) * (randn(size(txSig)) + 1i*randn(size(txSig)));

% Add the noise vector to the transmitted signal vector
rxSig = txSig + noise;
end