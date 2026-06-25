function [rxBits, rxSym, refConst] = demodulate_signal(rxSig, spec)
%DEMODULATE_SIGNAL  Complex baseband signal -> symbol decisions -> bits.

% Routes demodulation logic to match the transmitter
switch spec.type
    case "psk"
        % Maps the received noisy complex coordinates back to the closest
        % integer symbol
        rxSym = pskdemod(rxSig, spec.M, spec.phaseOffset, 'gray');
        refConst = pskmod((0:spec.M-1).', spec.M, spec.phaseOffset, 'gray');

    case "qam"
        rxSym = qamdemod(rxSig, spec.M, 'gray', UnitAveragePower=true);
        refConst = qammod((0:spec.M-1).', spec.M, 'gray', UnitAveragePower=true);

    case "genqam"
        refConst = get_8qam_constellation();
        rxSym = genqamdemod(rxSig, refConst);

    otherwise
        error('Unknown modulation type: %s', spec.type);
end

rxBits = symbols_to_bits(rxSym, spec.M);
rxBits = rxBits(:);
end

function const = get_8qam_constellation()
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

function bits = symbols_to_bits(sym, M)
k = log2(M);

% Forces the symbols into pure integers, stripping any residual 
% floating-point inaccuracies
sym = round(real(sym(:)));
bitMat = zeros(numel(sym), k);

for ii = 1:k
    bitMat(:, ii) = bitget(sym, k - ii + 1);
end

bits = reshape(bitMat.', [], 1);
end