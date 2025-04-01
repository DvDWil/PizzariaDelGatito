#include <stdio.h>
#include <string.h>
#include <ctype.h> // Para tolower()

#define MAX_CLIENTES 100
#define MAX_PEDIDOS 100
#define MAX_SABORES 14

typedef struct {
    char nome[50];
    char endereco[100];
    char telefone[20];
    char email[50];
    int pedidos_count;
} Cliente;

typedef struct {
    int numero_pedido;
    Cliente *cliente;
    char sabor1[50];
    char sabor2[50];
    char tamanho[10];
    int quantidade;
    float preco_total;
    char regiao[50];
    float frete;
} Pedido;

Cliente clientes[MAX_CLIENTES];
Pedido pedidos[MAX_PEDIDOS];
int cliente_count = 0;
int pedido_count = 0; // Adicionei um contador global de pedidos

const char sabores_disponiveis[MAX_SABORES][50] = {
    "Calabresa", "Mussarela", "Portuguesa", "Frango com Catupiry", "4 Queijos", 
    "Bacon Supreme", "Pepperoni", "Vegetariana", "Especial da Casa", 
    "Chocolate", "Chocolate com Morango", "Oreo", "Romeu e Julieta", "Banana com Canela"
};

const float precos_pizza[MAX_SABORES][3] = {
    {20.00, 30.00, 40.00}, // Calabresa
    {18.00, 28.00, 38.00}, // Mussarela
    {22.00, 32.00, 42.00}, // Portuguesa
    {21.00, 31.00, 41.00}, // Frango com Catupiry
    {24.00, 34.00, 44.00}, // 4 Queijos
    {37.00, 47.00, 57.00}, // Bacon Supreme
    {36.00, 46.00, 56.00}, // Pepperoni
    {35.00, 45.00, 55.00}, // Vegetariana
    {40.00, 50.00, 60.00}, // Especial da Casa
    {32.00, 42.00, 52.00}, // Chocolate
    {35.00, 45.00, 55.00}, // Chocolate com Morango
    {32.00, 42.00, 52.00}, // Oreo
    {35.00, 45.00, 55.00}, // Romeu e Julieta
    {33.00, 43.00, 53.00}  // Banana com Canela
};

const float precos_frete[7] = {5.00, 5.00, 10.00, 10.00, 15.00, 15.00, 0.00};
const char regioes[7][50] = {
    "Asa Sul", "Asa Norte", "Cruzeiro", "Sudoeste", "Octogonal", "Guará", "Retirar na Loja"
};

// Função para converter string para minúsculas (para comparação case-insensitive)
void toLowerCase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

float calcular_preco(const char* sabor1, const char* sabor2, const char* tamanho, int quantidade) {
    int sabor1_index = -1, sabor2_index = -1, tamanho_index = -1;
    char temp_tamanho[10];
    strcpy(temp_tamanho, tamanho);
    toLowerCase(temp_tamanho);

    // Encontrar os índices dos sabores
    for (int i = 0; i < MAX_SABORES; i++) {
        if (strcasecmp(sabores_disponiveis[i], sabor1) == 0) sabor1_index = i;
        if (strcasecmp(sabores_disponiveis[i], sabor2) == 0) sabor2_index = i;
    }

    // Identificar o tamanho da pizza
    if (strcmp(temp_tamanho, "pequena") == 0) tamanho_index = 0;
    else if (strcmp(temp_tamanho, "media") == 0) tamanho_index = 1;
    else if (strcmp(temp_tamanho, "grande") == 0) tamanho_index = 2;
    else {
        printf("Tamanho inválido!\n");
        return 0;
    }

    if (sabor1_index == -1) {
        printf("Sabor 1 inválido!\n");
        return 0;
    }
    if (sabor2_index == -1 && strcasecmp(sabor2, "Nenhum") != 0) {
        printf("Sabor 2 inválido!\n");
        return 0;
    }

    float preco = 0.0;

    if (sabor2_index == -1 || strcasecmp(sabor2, "Nenhum") == 0) {
        preco = precos_pizza[sabor1_index][tamanho_index];
    } else {
        preco = (precos_pizza[sabor1_index][tamanho_index] + precos_pizza[sabor2_index][tamanho_index]) / 2.0;
    }

    return preco * quantidade;
}

float calcular_frete(const char* regiao) {
    for (int i = 0; i < 7; i++) {
        if (strcasecmp(regioes[i], regiao) == 0) {
            return precos_frete[i];
        }
    }
    printf("Região inválida! Frete definido como 0.00\n");
    return 0.0;
}

Cliente* buscar_cliente(const char* email) {
    for (int i = 0; i < cliente_count; i++) {
        if (strcasecmp(clientes[i].email, email) == 0) {
            return &clientes[i];
        }
    }
    return NULL;
}

Cliente* registrar_cliente(const char* nome, const char* endereco, const char* telefone, const char* email) {
    // Verificar se cliente já existe
    Cliente* existente = buscar_cliente(email);
    if (existente != NULL) {
        return existente;
    }

    if (cliente_count >= MAX_CLIENTES) {
        printf("Limite de clientes atingido!\n");
        return NULL;
    }

    Cliente* novo_cliente = &clientes[cliente_count++];
    strncpy(novo_cliente->nome, nome, 49);
    novo_cliente->nome[49] = '\0';
    strncpy(novo_cliente->endereco, endereco, 99);
    novo_cliente->endereco[99] = '\0';
    strncpy(novo_cliente->telefone, telefone, 19);
    novo_cliente->telefone[19] = '\0';
    strncpy(novo_cliente->email, email, 49);
    novo_cliente->email[49] = '\0';
    novo_cliente->pedidos_count = 0;
    return novo_cliente;
}

void exibir_menu() {
    printf("\n=== MENU ===\n");
    printf("1. Fazer pedido\n");
    printf("2. Ver pedidos\n");
    printf("3. Sair\n");
    printf("Escolha uma opção: ");
}

void exibir_sabores() {
    printf("\nSabores disponíveis:\n");
    for (int i = 0; i < MAX_SABORES; i++) {
        printf("%d. %s\n", i+1, sabores_disponiveis[i]);
    }
}

void exibir_regioes() {
    printf("\nRegiões disponíveis:\n");
    for (int i = 0; i < 7; i++) {
        printf("%d. %s (Frete: R$%.2f)\n", i+1, regioes[i], precos_frete[i]);
    }
}

void fazer_pedido() {
    char nome[50], endereco[100], telefone[20], email[50];
    char sabor1[50], sabor2[50], tamanho[10], regiao[50];
    int quantidade, sabor_num;

    printf("\n=== NOVO PEDIDO ===\n");

    // Coletar informações do cliente
    printf("Digite seu email: ");
    fgets(email, 50, stdin);
    email[strcspn(email, "\n")] = '\0';

    Cliente* cliente = buscar_cliente(email);
    
    if (cliente == NULL) {
        printf("Cliente novo. Por favor, complete seu cadastro.\n");
        printf("Digite seu nome: ");
        fgets(nome, 50, stdin);
        nome[strcspn(nome, "\n")] = '\0';

        printf("Digite seu endereço: ");
        fgets(endereco, 100, stdin);
        endereco[strcspn(endereco, "\n")] = '\0';

        printf("Digite seu telefone: ");
        fgets(telefone, 20, stdin);
        telefone[strcspn(telefone, "\n")] = '\0';

        cliente = registrar_cliente(nome, endereco, telefone, email);
        if (cliente == NULL) {
            printf("Erro ao registrar cliente.\n");
            return;
        }
    } else {
        printf("Bem-vindo de volta, %s!\n", cliente->nome);
    }

    // Coletar informações do pedido
    exibir_sabores();
    
    printf("Escolha o número do sabor 1: ");
    scanf("%d", &sabor_num);
    getchar();
    if (sabor_num < 1 || sabor_num > MAX_SABORES) {
        printf("Sabor inválido!\n");
        return;
    }
    strcpy(sabor1, sabores_disponiveis[sabor_num-1]);

    printf("Escolha o número do sabor 2 (ou 0 para sabor único): ");
    scanf("%d", &sabor_num);
    getchar();
    if (sabor_num == 0) {
        strcpy(sabor2, "Nenhum");
    } else if (sabor_num < 1 || sabor_num > MAX_SABORES) {
        printf("Sabor inválido!\n");
        return;
    } else {
        strcpy(sabor2, sabores_disponiveis[sabor_num-1]);
    }

    printf("Escolha o tamanho (pequena, media, grande): ");
    fgets(tamanho, 10, stdin);
    tamanho[strcspn(tamanho, "\n")] = '\0';

    printf("Digite a quantidade: ");
    scanf("%d", &quantidade);
    getchar();

    exibir_regioes();
    printf("Escolha o número da região para entrega: ");
    scanf("%d", &sabor_num);
    getchar();
    if (sabor_num < 1 || sabor_num > 7) {
        printf("Região inválida!\n");
        return;
    }
    strcpy(regiao, regioes[sabor_num-1]);

    float preco_total = calcular_preco(sabor1, sabor2, tamanho, quantidade);
    float frete = calcular_frete(regiao);

    if (pedido_count >= MAX_PEDIDOS) {
        printf("Limite de pedidos atingido!\n");
        return;
    }

    Pedido novo_pedido = {
        pedido_count + 1,
        cliente,
        "", "", "", // Inicializa os sabores e tamanho
        quantidade,
        preco_total + frete,
        "",
        frete
    };
    
    // Copia as strings de forma segura
    strncpy(novo_pedido.sabor1, sabor1, 49);
    novo_pedido.sabor1[49] = '\0';
    strncpy(novo_pedido.sabor2, sabor2, 49);
    novo_pedido.sabor2[49] = '\0';
    strncpy(novo_pedido.tamanho, tamanho, 9);
    novo_pedido.tamanho[9] = '\0';
    strncpy(novo_pedido.regiao, regiao, 49);
    novo_pedido.regiao[49] = '\0';

    pedidos[pedido_count++] = novo_pedido;
    cliente->pedidos_count++;

    printf("\nPedido realizado com sucesso!\n");
    printf("Número do pedido: %d\n", novo_pedido.numero_pedido);
    printf("Preço total: R$%.2f (Frete: R$%.2f)\n", novo_pedido.preco_total, novo_pedido.frete);
}

void ver_pedidos() {
    if (pedido_count == 0) {
        printf("\nNenhum pedido registrado ainda.\n");
        return;
    }

    printf("\n=== TODOS OS PEDIDOS ===\n");
    for (int i = 0; i < pedido_count; i++) {
        printf("\nPedido %d:\n", pedidos[i].numero_pedido);
        printf("Cliente: %s\n", pedidos[i].cliente->nome);
        printf("Sabores: %s e %s\n", pedidos[i].sabor1, pedidos[i].sabor2);
        printf("Tamanho: %s, Quantidade: %d\n", pedidos[i].tamanho, pedidos[i].quantidade);
        printf("Região: %s, Frete: R$%.2f\n", pedidos[i].regiao, pedidos[i].frete);
        printf("Preço total: R$%.2f\n", pedidos[i].preco_total);
    }
}

int main() {
    int escolha;
    
    printf("=== SISTEMA DE PEDIDOS DE PIZZARIA ===\n");
    
    while (1) {
        exibir_menu();
        if (scanf("%d", &escolha) != 1) {
            printf("Entrada inválida! Por favor, digite um número.\n");
            while (getchar() != '\n'); // Limpa o buffer de entrada
            continue;
        }
        getchar(); // Consome o newline
        
        switch (escolha) {
            case 1:
                fazer_pedido();
                break;
            case 2:
                ver_pedidos();
                break;
            case 3:
                printf("Saindo...\n");
                return 0;
            default:
                printf("Opção inválida! Tente novamente.\n");
        }
    }
    
    return 0;
}