function plot_constellation(sig, plotTitle, refConst)
%PLOT_CONSTELLATION  Scatter plot of complex symbols.

sig = sig(:);

scatter(real(sig), imag(sig), 8, 'filled');
hold on;

% "nargin" stands for number of argument inputs (built-in func)
if nargin >= 3 && ~isempty(refConst)
    scatter(real(refConst(:)), imag(refConst(:)), 70, 'x', 'LineWidth', 1.5);
    legend('Samples', 'Reference constellation', 'Location', 'eastoutside');
else
    legend('Samples', 'Location', 'eastoutside');
end

grid on;
axis equal;
xlabel('In-Phase');
ylabel('Quadrature');
title(plotTitle);
hold off;
end