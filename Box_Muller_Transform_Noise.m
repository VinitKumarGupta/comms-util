% Define the number of samples
num_samples = 10000;

% Step 1: Generate independent uniform random variables on (0,1)
U1 = rand(num_samples, 1);
U2 = rand(num_samples, 1);

% Step 2: Apply the Box-Muller transformation formulas
R = sqrt(-2 * log(U1));
Theta = 2 * pi * U2;

Z0 = R .* cos(Theta); % First independent standard normal variable
Z1 = R .* sin(Theta); % Second independent standard normal variable

% Step 3: Shift and scale to non-standard normal distributions (Optional)
% To get a distribution with target mean (mu) and standard deviation (sigma):
mu = 5;
sigma = 2;
X0 = mu + sigma * Z0; 

% Step 4: Verify results by plotting a histogram
figure;
histogram(Z0, 50, 'Normalization', 'pdf');
hold on;
fplot(@(x) normpdf(x, 0, 1), [-4, 4], 'LineWidth', 2, 'Color', 'r');
title('Box-Muller Generated Standard Normal Distribution');
xlabel('Value');
ylabel('Probability Density');
legend('Generated Samples', 'Theoretical PDF');
grid on;