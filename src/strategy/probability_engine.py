def find_best_proposals(market, analysis):
    market_price = market.outcomes[0].price
    estimated_prob = analysis.probability
    
    edge = estimated_prob - market_price
    
    if edge > 0.10: # Recommend only if edge > 10%
        return {
            "question": market.question,
            "market_price": market_price,
            "ai_probability": estimated_prob,
            "edge": edge,
            "reasoning": analysis.reasoning
        }
    return None