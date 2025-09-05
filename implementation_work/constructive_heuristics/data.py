import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

RESULTS_FILE = 'results.txt'
OPTIMAL_FILE = 'optimal.txt'
PLOTS_DIR = 'plots'
sns.set_theme(style="whitegrid")

def load_data():
    try:
        results_data = []
        with open(RESULTS_FILE, 'r') as f:
            for line in f:
                if not line.strip(): continue
                parts = line.strip().split(': ')
                name = parts[0]
                values = parts[1].split()
                cost = int(values[0])
                time = int(values[1])
                results_data.append({
                    'Instancia': name.replace('.tsp', ''),
                    'Custo Obtido': cost,
                    'Tempo (ms)': time
                })
        results_df = pd.DataFrame(results_data)
        
        optimal_data = []
        with open(OPTIMAL_FILE, 'r') as f:
            for line in f:
                if not line.strip(): continue
                name, value = line.strip().split(': ')
                optimal_data.append({'Instancia': name.replace('.tsp', ''), 'Custo Otimo': int(value)})
        optimal_df = pd.DataFrame(optimal_data)
        
        combined_df = pd.merge(optimal_df, results_df, on='Instancia')
        
        combined_df['Gap (%)'] = ((combined_df['Custo Obtido'] - combined_df['Custo Otimo']) / combined_df['Custo Otimo']) * 100
        
        return combined_df

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e.filename}")
        print("Certifique-se que os arquivos 'results.txt' e 'optimal.txt' estão no mesmo diretório.")
        return None
    except (IndexError, ValueError) as e:
        print(f"Erro ao ler os arquivos: {e}")
        print("Verifique se o formato dos arquivos 'results.txt' e 'optimal.txt' está correto.")
        return None

def create_plots(df):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    
    df = df.sort_values('Instancia').reset_index(drop=True)

    plt.figure(figsize=(15, 8))
    plot_data = df.melt(id_vars='Instancia', value_vars=['Custo Obtido', 'Custo Otimo'], var_name='Tipo de Custo', value_name='Custo')
    sns.barplot(data=plot_data, x='Instancia', y='Custo', hue='Tipo de Custo', palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title('Comparação de Custos: Obtido vs. Ótimo', fontsize=16)
    plt.ylabel('Custo Total')
    plt.xlabel('Instância')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'comparacao_custos.png'))
    plt.close()
    print(f"Gráfico 'comparacao_custos.png' salvo em '{PLOTS_DIR}/'")

    plt.figure(figsize=(15, 8))
    ax = sns.barplot(data=df, x='Instancia', y='Gap (%)', palette='coolwarm')
    plt.xticks(rotation=45, ha='right')
    plt.title('Gap Percentual em Relação à Solução Ótima', fontsize=16)
    plt.ylabel('Gap (%)')
    plt.xlabel('Instância')
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', fontsize=9, color='black', xytext=(0, 5),
                    textcoords='offset points')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'gap_percentual.png'))
    plt.close()
    print(f"Gráfico 'gap_percentual.png' salvo em '{PLOTS_DIR}/'")

    plt.figure(figsize=(15, 8))
    sns.barplot(data=df, x='Instancia', y='Tempo (ms)', palette='plasma')
    plt.xticks(rotation=45, ha='right')
    plt.title('Tempo de Execução por Instância', fontsize=16)
    plt.ylabel('Tempo (milissegundos)')
    plt.xlabel('Instância')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'tempo_execucao.png'))
    plt.close()
    print(f"Gráfico 'tempo_execucao.png' salvo em '{PLOTS_DIR}/'")

if __name__ == "__main__":
    data_df = load_data()
    if data_df is not None and not data_df.empty:
        create_plots(data_df)
        
        print("\n--- Análise Resumida ---")
        print(f"Média do Gap Percentual: {data_df['Gap (%)'].mean():.2f}%")
        print(f"Pior Gap: {data_df['Gap (%)'].max():.2f}% (Instância: {data_df.loc[data_df['Gap (%)'].idxmax()]['Instancia']})")
        print(f"Melhor Gap: {data_df['Gap (%)'].min():.2f}% (Instância: {data_df.loc[data_df['Gap (%)'].idxmin()]['Instancia']})")
        print(f"Tempo total de execução: {data_df['Tempo (ms)'].sum() / 1000:.2f} segundos")
    elif data_df is not None:
        print("\nNão foram encontrados dados para processar. Verifique os arquivos de entrada.")