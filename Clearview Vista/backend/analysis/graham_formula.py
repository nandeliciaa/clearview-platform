#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo para cálculo do valor justo de ações usando a fórmula de Graham.
Este módulo implementa diferentes variações da fórmula de Graham para
avaliação de ações com base em indicadores fundamentalistas.
"""

import math
import numpy as np

def calculate_basic_graham(eps, bvps):
    """
    Calcula o valor justo usando a fórmula básica de Graham.
    
    Fórmula: √(22.5 * EPS * BVPS)
    Onde:
    - EPS (Earnings Per Share): Lucro por Ação
    - BVPS (Book Value Per Share): Valor Patrimonial por Ação
    
    Args:
        eps (float): Lucro por Ação
        bvps (float): Valor Patrimonial por Ação
        
    Returns:
        float: Valor justo calculado
    """
    if eps <= 0 or bvps <= 0:
        return 0
    
    return math.sqrt(22.5 * eps * bvps)

def calculate_extended_graham(eps, bvps, growth_rate=0, bond_yield=0.05):
    """
    Calcula o valor justo usando a fórmula estendida de Graham.
    
    Fórmula: (EPS * (8.5 + 2g) * 4.4) / Y
    Onde:
    - EPS: Lucro por Ação
    - g: Taxa de crescimento esperada (em decimal)
    - Y: Rendimento de títulos AAA (em decimal)
    
    Args:
        eps (float): Lucro por Ação
        bvps (float): Valor Patrimonial por Ação (não usado nesta fórmula, mas mantido para consistência)
        growth_rate (float): Taxa de crescimento esperada (em decimal)
        bond_yield (float): Rendimento de títulos AAA (em decimal)
        
    Returns:
        float: Valor justo calculado
    """
    if eps <= 0 or bond_yield <= 0:
        return 0
    
    # Limitar a taxa de crescimento a 15% conforme recomendação de Graham
    capped_growth = min(growth_rate, 0.15)
    
    return (eps * (8.5 + 2 * capped_growth * 100) * 4.4) / (bond_yield * 100)

def calculate_brazilian_graham(eps, bvps, roe=0, dividend_yield=0, debt_to_ebitda=None):
    """
    Calcula o valor justo usando uma adaptação da fórmula de Graham para o mercado brasileiro.
    
    Esta versão considera fatores adicionais relevantes para o mercado brasileiro:
    - ROE (Return on Equity)
    - Dividend Yield
    - Relação Dívida/EBITDA
    
    Args:
        eps (float): Lucro por Ação
        bvps (float): Valor Patrimonial por Ação
        roe (float): Retorno sobre Patrimônio Líquido (em decimal)
        dividend_yield (float): Dividend Yield (em decimal)
        debt_to_ebitda (float): Relação Dívida/EBITDA
        
    Returns:
        float: Valor justo calculado
    """
    if eps <= 0 or bvps <= 0:
        return 0
    
    # Calcular valor base usando a fórmula básica
    base_value = math.sqrt(22.5 * eps * bvps)
    
    # Ajustar com base no ROE
    # Empresas com ROE maior merecem um prêmio
    roe_factor = 1.0
    if roe > 0.20:  # ROE > 20%
        roe_factor = 1.3
    elif roe > 0.15:  # ROE > 15%
        roe_factor = 1.2
    elif roe > 0.10:  # ROE > 10%
        roe_factor = 1.1
    elif roe < 0.05:  # ROE < 5%
        roe_factor = 0.8
    
    # Ajustar com base no Dividend Yield
    # Empresas com maior dividend yield merecem um prêmio
    dy_factor = 1.0
    if dividend_yield > 0.07:  # DY > 7%
        dy_factor = 1.2
    elif dividend_yield > 0.05:  # DY > 5%
        dy_factor = 1.1
    elif dividend_yield < 0.02:  # DY < 2%
        dy_factor = 0.9
    
    # Ajustar com base na relação Dívida/EBITDA
    # Empresas menos endividadas merecem um prêmio
    debt_factor = 1.0
    if debt_to_ebitda is not None:
        if debt_to_ebitda > 3.0:
            debt_factor = 0.8
        elif debt_to_ebitda > 2.0:
            debt_factor = 0.9
        elif debt_to_ebitda < 1.0:
            debt_factor = 1.1
    
    # Aplicar todos os fatores ao valor base
    adjusted_value = base_value * roe_factor * dy_factor * debt_factor
    
    return adjusted_value

def calculate_graham_score(price, fair_value, pe_ratio, pb_ratio, roe, dividend_yield, debt_to_ebitda=None):
    """
    Calcula uma pontuação para a ação com base nos critérios de Graham.
    
    Args:
        price (float): Preço atual da ação
        fair_value (float): Valor justo calculado
        pe_ratio (float): Índice Preço/Lucro
        pb_ratio (float): Índice Preço/Valor Patrimonial
        roe (float): Retorno sobre Patrimônio Líquido (em decimal)
        dividend_yield (float): Dividend Yield (em decimal)
        debt_to_ebitda (float): Relação Dívida/EBITDA
        
    Returns:
        dict: Pontuação e classificação da ação
    """
    score = 0
    strengths = []
    weaknesses = []
    
    # Avaliar relação entre preço e valor justo
    if fair_value > 0:
        potential = ((fair_value - price) / price) * 100
        if potential > 50:
            score += 3
            strengths.append(f"Potencial de valorização excepcional: {potential:.1f}%")
        elif potential > 25:
            score += 2
            strengths.append(f"Alto potencial de valorização: {potential:.1f}%")
        elif potential > 10:
            score += 1
            strengths.append(f"Bom potencial de valorização: {potential:.1f}%")
        elif potential < -10:
            score -= 1
            weaknesses.append(f"Potencial de valorização negativo: {potential:.1f}%")
        elif potential < -25:
            score -= 2
            weaknesses.append(f"Ação significativamente sobreavaliada: {potential:.1f}%")
    
    # Avaliar P/L
    if pe_ratio > 0:
        if pe_ratio < 10:
            score += 2
            strengths.append(f"P/L baixo: {pe_ratio:.1f}")
        elif pe_ratio < 15:
            score += 1
            strengths.append(f"P/L moderado: {pe_ratio:.1f}")
        elif pe_ratio > 25:
            score -= 1
            weaknesses.append(f"P/L alto: {pe_ratio:.1f}")
        elif pe_ratio > 40:
            score -= 2
            weaknesses.append(f"P/L muito alto: {pe_ratio:.1f}")
    
    # Avaliar P/VP
    if pb_ratio > 0:
        if pb_ratio < 1:
            score += 2
            strengths.append(f"P/VP abaixo de 1: {pb_ratio:.1f}")
        elif pb_ratio < 1.5:
            score += 1
            strengths.append(f"P/VP moderado: {pb_ratio:.1f}")
        elif pb_ratio > 3:
            score -= 1
            weaknesses.append(f"P/VP alto: {pb_ratio:.1f}")
        elif pb_ratio > 5:
            score -= 2
            weaknesses.append(f"P/VP muito alto: {pb_ratio:.1f}")
    
    # Avaliar ROE
    if roe > 0:
        if roe > 0.20:
            score += 2
            strengths.append(f"ROE excelente: {roe*100:.1f}%")
        elif roe > 0.15:
            score += 1
            strengths.append(f"ROE bom: {roe*100:.1f}%")
        elif roe < 0.08:
            score -= 1
            weaknesses.append(f"ROE baixo: {roe*100:.1f}%")
        elif roe < 0.05:
            score -= 2
            weaknesses.append(f"ROE muito baixo: {roe*100:.1f}%")
    
    # Avaliar Dividend Yield
    if dividend_yield > 0:
        if dividend_yield > 0.07:
            score += 2
            strengths.append(f"Dividend Yield excelente: {dividend_yield*100:.1f}%")
        elif dividend_yield > 0.05:
            score += 1
            strengths.append(f"Dividend Yield bom: {dividend_yield*100:.1f}%")
    
    # Avaliar Dívida/EBITDA
    if debt_to_ebitda is not None:
        if debt_to_ebitda < 1:
            score += 2
            strengths.append(f"Endividamento muito baixo: {debt_to_ebitda:.1f}x")
        elif debt_to_ebitda < 2:
            score += 1
            strengths.append(f"Endividamento baixo: {debt_to_ebitda:.1f}x")
        elif debt_to_ebitda > 3:
            score -= 1
            weaknesses.append(f"Endividamento alto: {debt_to_ebitda:.1f}x")
        elif debt_to_ebitda > 4:
            score -= 2
            weaknesses.append(f"Endividamento muito alto: {debt_to_ebitda:.1f}x")
    
    # Determinar classificação com base na pontuação
    if score >= 6:
        rating = "Ótima Oportunidade"
    elif score >= 3:
        rating = "Compra"
    elif score >= 0:
        rating = "Manter"
    elif score >= -3:
        rating = "Neutro"
    else:
        rating = "Venda"
    
    # Verificar se é uma ótima oportunidade (70% do valor justo)
    if fair_value > 0 and price <= 0.7 * fair_value:
        if rating != "Ótima Oportunidade":
            rating = "Ótima Oportunidade"
            strengths.append("Cotada abaixo de 70% do valor justo")
    
    return {
        "score": score,
        "rating": rating,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "potential": potential if fair_value > 0 else 0
    }

# Função para teste
def main():
    # Exemplo de uso
    eps = 2.5  # Lucro por Ação
    bvps = 15.0  # Valor Patrimonial por Ação
    price = 25.0  # Preço atual
    
    # Calcular valor justo usando diferentes métodos
    basic_value = calculate_basic_graham(eps, bvps)
    extended_value = calculate_extended_graham(eps, bvps, 0.10, 0.05)
    brazilian_value = calculate_brazilian_graham(eps, bvps, 0.18, 0.06, 1.5)
    
    print(f"Valor Justo (Fórmula Básica): R$ {basic_value:.2f}")
    print(f"Valor Justo (Fórmula Estendida): R$ {extended_value:.2f}")
    print(f"Valor Justo (Adaptação Brasileira): R$ {brazilian_value:.2f}")
    
    # Calcular pontuação
    score = calculate_graham_score(
        price=price,
        fair_value=brazilian_value,
        pe_ratio=price/eps,
        pb_ratio=price/bvps,
        roe=0.18,
        dividend_yield=0.06,
        debt_to_ebitda=1.5
    )
    
    print(f"\nPontuação: {score['score']}")
    print(f"Classificação: {score['rating']}")
    print(f"Potencial: {score['potential']:.1f}%")
    
    print("\nPontos Fortes:")
    for strength in score['strengths']:
        print(f"- {strength}")
    
    print("\nPontos Fracos:")
    for weakness in score['weaknesses']:
        print(f"- {weakness}")

if __name__ == "__main__":
    main()
