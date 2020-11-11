//
// Created by liuyekuan on 2020/5/16.
//

#ifndef ALPHAZERO_RENJU_STRATEGY_H
#define ALPHAZERO_RENJU_STRATEGY_H

#include <tuple>
#include "cpp/src/data_structure/data_structure.h"
#include "cpp/src/board.h"
#include <random>

class Strategy {
public:
    virtual std::tuple<int, int> step(const Board& board) = 0;
};

class RandomStrategy: public Strategy {
private:
    std::mt19937 rng;
public:
    RandomStrategy();

    std::tuple<int, int> step(const Board& board) override;
};

class MctsStrategy: public Strategy {
public:
    MctsStrategy(MODEL_TYPE model_type);

    std::tuple<int, int> step(const Board& board) override;
};

#endif //ALPHAZERO_RENJU_STRATEGY_H
