function [txSig, txBitsPadded, padBits, txSym, refConst] = modulate_signal(bitsIn, spec)
%MODULATE_SIGNAL  Bit -> symbol -> complex baseband signal.

bitsIn = bitsIn(:); % Ensures the input bit array is a column vector
k = log2(spec.M);

[txSym, txBitsPadded, padBits] = bits_to_symbols(bitsIn, k);

switch spec.type
    case "psk"
        txSig = pskmod(txSym, spec.M, spec.phaseOffset, 'gray');
        refConst = pskmod((0:spec.M-1).', spec.M, spec.phaseOffset, 'gray');

    case "qam"
        txSig = qammod(txSym, spec.M, 'gray', UnitAveragePower=true);
        refConst = qammod((0:spec.M-1).', spec.M, 'gray', UnitAveragePower=true);

    case "genqam"
        refConst = get_8qam_constellation();
        txSig = genqammod(txSym, refConst);

    otherwise
        error('Unknown modulation type: %s', spec.type);
end
end

function const = get_8qam_constellation()
% A simple cross 8-QAM constellation, normalized to unit average power.
const = [
    -1 - 1i
    -1 + 1i
     1 + 1i
     1 - 1i
    -3 + 0i
     0 + 3i
     3 + 0i
     0 - 3i
];
const = const / sqrt(mean(abs(const).^2));
end

function [sym, bitsPadded, padBits] = bits_to_symbols(bitsIn, k)
bitsIn = bitsIn(:);

% highly optimized mathematical trick to calculate how many zeros 
% are needed to make the total bit count perfectly divisible by k.
padBits = mod(-numel(bitsIn), k);

bitsPadded = [bitsIn; zeros(padBits,1)];    % Appends the padding zeros

% Reshapes the vector into a matrix where each row 
% represents one symbol's bits
bitMat = reshape(bitsPadded, k, []).';

% Creates binary weighting values (e.g., for 3 bits: 4, 2, 1)
weights = 2.^(k-1:-1:0);

% Performs matrix multiplication to convert binary rows 
% into integer decimal symbols rapidly.
sym = bitMat * weights.';
sym = sym(:);
end