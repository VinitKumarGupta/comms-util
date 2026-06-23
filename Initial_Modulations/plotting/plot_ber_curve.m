function plot_ber_curve(EbNoVec, results)
%PLOT_BER_CURVE  Overlay simulated and theoretical BER curves.

hold on;

colors = {
    [0 0.4470 0.7410]      % blue
    [0.8500 0.3250 0.0980] % orange/red
    [0.4660 0.6740 0.1880] % green
    [0.4940 0.1840 0.5560] % purple
    [0.3010 0.7450 0.9330] % cyan
    [0 0 0]                % black
};

for i = 1:numel(results)
    semilogy(EbNoVec, results{i}.berSim, '-o', ...
    'Color', colors{i}, ...
    'LineWidth', 1.6, ...
    'DisplayName', results{i}.name + " Sim");

    if isfield(results{i}, 'berTheory') && ~all(isnan(results{i}.berTheory))
        semilogy(EbNoVec, results{i}.berTheory, '--', ...
            'Color', colors{i}, ...
            'LineWidth', 1.6, ...
            'DisplayName', results{i}.name + " Theory");
    end

end

grid on;
grid minor;
set(gca,'YScale','log');    % forces the Y-axis to logarithmic scale
ylim([1e-6 1]);

xlabel('Eb/N0 (dB)');
ylabel('BER');
title('BER vs Eb/N0');
legend('Location', 'eastoutside');
hold off;
end