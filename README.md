# Flux Hub: Autonomous UCP Agent for Agentic Commerce 🚀

**Flux Hub** é uma prova de conceito de um orquestrador de compras autônomo baseado no **Universal Commerce Protocol (UCP)**. Utilizando o modelo **Gemini 2.0 Flash**, o agente é capaz de descobrir mercantes, comparar ofertas e executar pagamentos usando mandatos pré-aprovados.

## 🌟 Diferenciais Técnicos
- **Autonomous Discovery:** Varredura dinâmica de endpoints `.well-known/ucp`.
- **Decision Making:** Lógica de comparação de preços entre múltiplos fornecedores.
- **Mandate-Based Payment:** Execução de transações financeiras automáticas baseadas em limites de crédito (Mandatos).
- **Multi-turn Tool Use:** Orquestração de chamadas de API sequenciais (Discovery -> Checkout -> Pay -> Status).

## 🏗️ Arquitetura
O sistema é dividido em dois domínios:
1. **The Hub (Agent):** O cérebro que processa linguagem natural e gerencia ferramentas (tools).
2. **The Ecosystem (Merchants):** Simuladores de APIs de e-commerce que expõem capacidades via UCP.

```mermaid
sequenceDiagram
    participant User
    participant FluxHub as Gemini Agent
    participant Merchants as Store APIs (8182, 8183, 8184)
    
    User->>FluxHub: "Encontre a melhor oferta de Camiseta"
    FluxHub->>Merchants: discovery_ucp()
    Merchants-->>FluxHub: Offers JSON (Price Comparison)
    FluxHub->>FluxHub: Decide: Best Offer (Port 8183)
    FluxHub->>Merchants: create_checkout()
    FluxHub->>Merchants: authorize_payment() (Mandate Approval)
    FluxHub->>Merchants: check_payment_status()
```
    FluxHub-->>User: Final Transaction Report (PAID)
