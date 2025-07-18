import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Configurações gerais
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'

# Dados completos para cálculo estatístico
raw_data = {
    'Polygon': {
        'Cost': [0.000384, 0.000384, 0.000722],
        'Efficiency': [98.78, 98.78, 98.78]
    },
    'Arbitrum': {
        'Cost': [0.001121, 0.002934, 0.001123],
        'Efficiency': [97.71, 79.67, 97.71]
    },
    'Optimism': {
        'Cost': [0.003716, 0.000318, 0.000151],
        'Efficiency': [100, 100, 98.92]
    }
}

# Calcular estatísticas (média e intervalo de confiança 95%)
networks = ['Polygon', 'Arbitrum', 'Optimism']
metrics = {
    'Cost (USD)': [],
    'Efficiency (%)': [],
    'Cost_CI': [],
    'Efficiency_CI': []
}

for network in networks:
    # Cálculo para custo
    cost_data = raw_data[network]['Cost']
    cost_mean = np.mean(cost_data)
    cost_std = np.std(cost_data, ddof=1)  # Desvio padrão amostral
    cost_ci = stats.t.interval(0.1, len(cost_data)-1, loc=cost_mean, scale=stats.sem(cost_data))
    
    # Cálculo para eficiência
    eff_data = raw_data[network]['Efficiency']
    eff_mean = np.mean(eff_data)
    eff_std = np.std(eff_data, ddof=1)
    eff_ci = stats.t.interval(0.1, len(eff_data)-1, loc=eff_mean, scale=stats.sem(eff_data))
    
    metrics['Cost (USD)'].append(cost_mean)
    metrics['Efficiency (%)'].append(eff_mean)
    metrics['Cost_CI'].append((cost_mean - cost_ci[0], cost_ci[1] - cost_mean))  # (lower_diff, upper_diff)
    metrics['Efficiency_CI'].append((eff_mean - eff_ci[0], eff_ci[1] - eff_mean))

# Paleta de cores
colors = ['#8A2BE2', '#1E90FF', '#FF4500']

# Criando figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='white')

# Gráfico 1: Custo em USD com intervalo de confiança
for i, (network, color) in enumerate(zip(networks, colors)):
    cost = metrics['Cost (USD)'][i]
    ci_lower, ci_upper = metrics['Cost_CI'][i]
    
    bar = ax1.bar(i, cost, color=color, edgecolor='black', linewidth=0.7, 
                 width=0.6, alpha=0.9, zorder=3)
    
    ax1.errorbar(i, cost, yerr=[[ci_lower], [ci_upper]], 
                fmt='none', ecolor='#333333', elinewidth=1.5, capsize=5, capthick=1.5, zorder=4)
    
    ax1.text(i, cost + 0.0001, f'${cost:.4f}', ha='center', 
            fontsize=10, fontweight='bold', color='#333333', zorder=5)

ax1.set_title('A) Transaction Cost', fontsize=12, fontweight='bold', pad=15)
ax1.set_ylabel('Cost (USD)', fontsize=11)
ax1.set_xticks(range(len(networks)))
ax1.set_xticklabels(networks, fontsize=11)
ax1.set_ylim(0, 0.005)
ax1.yaxis.grid(True, linestyle=':', alpha=0.5, zorder=1)

# Gráfico 2: Eficiência com intervalo de confiança
for i, (network, color) in enumerate(zip(networks, colors)):
    eff = metrics['Efficiency (%)'][i]
    ci_lower, ci_upper = metrics['Efficiency_CI'][i]
    
    bar = ax2.bar(i, eff, color=color, edgecolor='black', linewidth=0.7, 
                 width=0.6, alpha=0.9, zorder=3)
    
    ax2.errorbar(i, eff, yerr=[[ci_lower], [ci_upper]], 
                fmt='none', ecolor='#333333', elinewidth=1.5, capsize=5, capthick=1.5, zorder=4)
    
    ax2.text(i, eff + 2, f'{eff:.1f}%', ha='center', 
            fontsize=10, fontweight='bold', color='#333333', zorder=5)

ax2.set_title('B) Gas Efficiency', fontsize=12, fontweight='bold', pad=15)
ax2.set_ylabel('Efficiency (%)', fontsize=11)
ax2.set_xticks(range(len(networks)))
ax2.set_xticklabels(networks, fontsize=11)
ax2.set_ylim(70, 105)
ax2.yaxis.grid(True, linestyle=':', alpha=0.5, zorder=1)

# Ajustes finais
plt.tight_layout(pad=3)

# Legenda
legend_elements = [
    plt.Rectangle((0,0), 1, 1, fc=colors[0], edgecolor='black'),
    plt.Rectangle((0,0), 1, 1, fc=colors[1], edgecolor='black'),
    plt.Rectangle((0,0), 1, 1, fc=colors[2], edgecolor='black')
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

plt.savefig('delegate_analysis_with_CI.png', dpi=300, bbox_inches='tight', facecolor='white')
