import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Configurações gerais
plt.style.use('default')
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.edgecolor': '#333333',
    'axes.facecolor': 'white',
    'figure.facecolor': 'white'
})

# Dados completos para cálculo estatístico
raw_data = {
    'Polygon': {
        'Cost': [0.000189, 0.000151, 0.000285],
        'Efficiency': [79.67, 79.67, 79.67]
    },
    'Arbitrum': {
        'Cost': [0.000476, 0.001605, 0.000564],
        'Efficiency': [96.36, 75.67, 95.93]
    },
    'Optimism': {
        'Cost': [0.000117, 0.000120, 0.003729],
        'Efficiency': [79.67, 98.80, 79.67]
    }
}

# Função segura para calcular intervalos de confiança
def safe_ci(data, confidence=0.1):
    data = np.array(data)
    if len(data) < 2 or np.all(data == data[0]):  # Se todos valores forem iguais
        return (data[0], data[0])
    
    try:
        ci = stats.t.interval(confidence, len(data)-1, 
                            loc=np.mean(data), 
                            scale=stats.sem(data, nan_policy='omit'))
        return ci
    except:
        return (np.min(data), np.max(data))

# Calcular estatísticas
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
    cost_ci = safe_ci(cost_data)
    metrics['Cost (USD)'].append(cost_mean)
    metrics['Cost_CI'].append((cost_mean - cost_ci[0], cost_ci[1] - cost_mean))
    
    # Cálculo para eficiência
    eff_data = raw_data[network]['Efficiency']
    eff_mean = np.mean(eff_data)
    eff_ci = safe_ci(eff_data)
    metrics['Efficiency (%)'].append(eff_mean)
    metrics['Efficiency_CI'].append((eff_mean - eff_ci[0], eff_ci[1] - eff_mean))

# Paleta de cores
colors = ['#8A2BE2', '#1E90FF', '#FF4500']

# Criando figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='white')

### Gráfico 1: Custo em USD ###
for i, (network, color) in enumerate(zip(networks, colors)):
    cost = metrics['Cost (USD)'][i]
    ci_lower, ci_upper = metrics['Cost_CI'][i]
    
    bar = ax1.bar(i, cost, color=color, edgecolor='black', linewidth=0.7, 
                 width=0.65, alpha=0.9, zorder=3)
    
    # Desenhar barras de erro apenas se houver variação
    if ci_lower + ci_upper > 0:
        ax1.errorbar(i, cost, yerr=[[ci_lower], [ci_upper]], 
                    fmt='none', ecolor='#333333', elinewidth=1.5, 
                    capsize=5, capthick=1.5, zorder=4)
    
    ax1.text(i, cost + 0.0001, f'${cost:.5f}', ha='center', 
            fontsize=10, fontweight='bold', color='#333333', zorder=5)

ax1.set_title('A) Revoke Operation Cost', fontsize=12, 
             fontweight='bold', pad=15)
ax1.set_ylabel('Cost (USD)', fontsize=11, labelpad=10)
ax1.set_xticks(range(len(networks)))
ax1.set_xticklabels(networks, fontsize=11)
ax1.set_ylim(0, 0.0045)
ax1.yaxis.grid(True, linestyle=':', alpha=0.5)

### Gráfico 2: Eficiência vs Custo ###
for i, (network, color) in enumerate(zip(networks, colors)):
    eff = metrics['Efficiency (%)'][i]
    cost = metrics['Cost (USD)'][i]
    eff_ci = metrics['Efficiency_CI'][i]
    cost_ci = metrics['Cost_CI'][i]
    
    # Ponto principal
    ax2.scatter(eff, cost, c=color, s=200, alpha=0.8, zorder=3)
    
    # Barras de erro (apenas se houver variação)
    if eff_ci[0] + eff_ci[1] > 0 or cost_ci[0] + cost_ci[1] > 0:
        ax2.errorbar(eff, cost, 
                    xerr=[[eff_ci[0]], [eff_ci[1]]] if eff_ci[0] + eff_ci[1] > 0 else None,
                    yerr=[[cost_ci[0]], [cost_ci[1]]] if cost_ci[0] + cost_ci[1] > 0 else None,
                    fmt='none', ecolor=color, elinewidth=1.5, 
                    capsize=5, alpha=0.7, zorder=2)
    
    ax2.text(eff + 1.5, cost + 0.0001, network, 
            fontsize=10, color=color, weight='bold', zorder=5)

ax2.set_title('B) Efficiency vs Cost', fontsize=12, 
            fontweight='bold', pad=15)
ax2.set_xlabel('Gas Efficiency (%)', fontsize=11)
ax2.set_ylabel('Cost (USD)', fontsize=11)
ax2.set_xlim(70, 105)
ax2.set_ylim(0, 0.0045)
ax2.grid(True, linestyle=':', alpha=0.7)

### Ajustes Finais ###
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

plt.savefig('revoke_analysis_final.png', dpi=300, bbox_inches='tight', facecolor='white')
