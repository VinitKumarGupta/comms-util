function [ber, numErr] = compute_ber(txBits, rxBits)
%COMPUTE_BER  Bit error rate from two binary vectors.

txBits = txBits(:);
rxBits = rxBits(:);

n = min(numel(txBits), numel(rxBits));
txBits = txBits(1:n);
rxBits = rxBits(1:n);

numErr = sum(txBits ~= rxBits);
ber = numErr / n;
end