import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Configuração inicial
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'

# Dados completos para cálculo estatístico
raw_data = {
    'Polygon': {
        'Cost': [0.000848, 0.000841, 0.002080],
        'Gas': [152.577, 152.577, 186.777]
    },
    'Arbitrum': {
        'Cost': [0.002423, 0.007076, 0.002421],
        'Gas': [157.560, 297.385, 157.544]
    },
    'Optimism': {
        'Cost': [0.000656, 0.001180, 0.000642],
        'Gas': [152.577, 186.777, 152.577]
    }
}

# Calcular estatísticas (média e intervalo de confiança 95%)
networks = ['Polygon', 'Arbitrum', 'Optimism']
metrics = {
    'Cost (USD)': [],
    'Gas Used (k)': [],
    'Cost_CI': [],
    'Gas_CI': []
}

for network in networks:
    # Cálculo para custo
    cost_data = raw_data[network]['Cost']
    cost_mean = np.mean(cost_data)
    cost_ci = stats.t.interval(0.1, len(cost_data)-1, loc=cost_mean, scale=stats.sem(cost_data))
    
    # Cálculo para consumo de gás
    gas_data = raw_data[network]['Gas']
    gas_mean = np.mean(gas_data)
    gas_ci = stats.t.interval(0.1, len(gas_data)-1, loc=gas_mean, scale=stats.sem(gas_data))
    
    metrics['Cost (USD)'].append(cost_mean)
    metrics['Gas Used (k)'].append(gas_mean)
    metrics['Cost_CI'].append((cost_mean - cost_ci[0], cost_ci[1] - cost_mean))
    metrics['Gas_CI'].append((gas_mean - gas_ci[0], gas_ci[1] - gas_mean))

# Cores
colors = ['#8A2BE2', '#1E90FF', '#FF4500']

# Criando figura com dois subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='white')

### Gráfico 1: Custo em USD com IC ###
for i, (network, color) in enumerate(zip(networks, colors)):
    cost = metrics['Cost (USD)'][i]
    ci_lower, ci_upper = metrics['Cost_CI'][i]
    
    bar = ax1.bar(i, cost, color=color, edgecolor='black', linewidth=0.7, width=0.65, alpha=0.9, zorder=3)
    ax1.errorbar(i, cost, yerr=[[ci_lower], [ci_upper]], 
                fmt='none', ecolor='#333333', elinewidth=1.5, capsize=5, capthick=1.5, zorder=4)
    ax1.text(i, cost + 0.0002, f'${cost:.4f}', ha='center', fontsize=10, fontweight='bold', color='black', zorder=5)

ax1.set_title('A) Mint Operation Cost', fontsize=12, fontweight='bold', pad=15)
ax1.set_ylabel('Cost (USD)', fontsize=11)
ax1.set_xticks(range(len(networks)))
ax1.set_xticklabels(networks, fontsize=11)
ax1.set_ylim(0, 0.0085)
ax1.yaxis.grid(True, linestyle='--', alpha=0.6, zorder=1)

### Gráfico 2: Consumo de Gás com IC ###
for i, (network, color) in enumerate(zip(networks, colors)):
    gas = metrics['Gas Used (k)'][i]
    ci_lower, ci_upper = metrics['Gas_CI'][i]
    
    bar = ax2.bar(i, gas, color=color, edgecolor='black', linewidth=0.7, width=0.65, alpha=0.9, zorder=3)
    ax2.errorbar(i, gas, yerr=[[ci_lower], [ci_upper]], 
                fmt='none', ecolor='#333333', elinewidth=1.5, capsize=5, capthick=1.5, zorder=4)
    ax2.text(i, gas + 5, f'{gas:.1f}k', ha='center', fontsize=10, fontweight='bold', color='black', zorder=5)

ax2.set_title('B) Gas Consumption', fontsize=12, fontweight='bold', pad=15)
ax2.set_ylabel('Gas Units (thousands)', fontsize=11)
ax2.set_xticks(range(len(networks)))
ax2.set_xticklabels(networks, fontsize=11)
ax2.set_ylim(0, 350)
ax2.yaxis.grid(True, linestyle='--', alpha=0.6, zorder=1)

### Ajustes finais ###
plt.tight_layout(pad=3)

# Legenda explicativa
legend_elements = [
    plt.Rectangle((0, 0), 1, 1, fc=colors[0], edgecolor='black'),
    plt.Rectangle((0, 0), 1, 1, fc=colors[1], edgecolor='black'),
    plt.Rectangle((0, 0), 1, 1, fc=colors[2], edgecolor='black')
]

fig.legend(legend_elements,
           ['Polygon (Sidechain)', 'Arbitrum (Rollup)', 'Optimism (Rollup)'],
           loc='lower center',
           bbox_to_anchor=(0.5, -0.08),
           ncol=3,
           frameon=True,
           facecolor='white',
           edgecolor='#cccccc',
           fontsize=10)

plt.savefig('nft_mint_analysis_with_CI.png', dpi=300, bbox_inches='tight', facecolor='white')
