import hashlib
import json
import time


class Transaction:
    def __init__(self, tx_from, tx_to, amount):
        self.tx_from = tx_from
        self.tx_to = tx_to
        self.amount = amount


class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        # use for compute a hash
        self.nonce = 1
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        计算`data`的哈希值
        :return:
        """
        return hashlib.sha256((
                                      str(self.transactions) +
                                      self.previous_hash +
                                      str(self.nonce) +
                                      str(self.timestamp)
                              ).encode("utf-8")).hexdigest()

    def get_head_string (self, difficulty):
        string = "0" * difficulty
        return string

    def mine(self, difficulty):
        """
        Blocked compute a hash until it conform the difficulty.
        :param difficulty:
        :return:
        """
        while True:
            if str(self.compute_hash())[0: difficulty] != self.get_head_string(difficulty):
                self.nonce += 1
                self.hash = self.compute_hash()
            else:
                break


class Chain:
    def __init__(self, difficulty):
        """
        chain      : You know, the block chain.
        difficulty : The difficulty of create a new block.
        """
        self.chain = [self.genesis()]
        self.transaction_pool = []
        self.miner_reward = 50
        self.difficulty = difficulty

    def genesis(self):
        """
        生成祖先区块
        :return: Block
        """
        genesis_block = Block("Genesis", "")
        return genesis_block

    def add_block(self, block):
        """
        Add a new block to chain which satisfies some conditions, such as proof of work algorithm.
        :param block:
        :return:
        """
        block.previous_hash = self.get_latest_block().hash
        # block.hash = block.compute_hash()
        block.mine(self.difficulty)
        self.chain.append(block)

    def add_transaction(self, tx):
        self.transaction_pool.append(tx)
        return self

    def mine_transaction_pool(self, miner_reward_address):
        # 1.发放旷工奖励
        miner_reward_tx = Transaction("Coin official", miner_reward_address, self.miner_reward)
        self.transaction_pool.append(miner_reward_tx)
        # 2.挖矿
        new_block = Block(self.transaction_pool, self.get_latest_block().previous_hash)
        new_block.mine(self.difficulty)
        # 3.将新块加到链上
        self.chain.append(new_block)
        # 4.清空交易池
        self.transaction_pool = []

    def get_latest_block(self):
        """
        获取最新的区块
        :return:
        """
        return self.chain[self.chain.__len__() - 1]

    def validate(self):
        """
        校验区块链
        :return: validate : True , otherwise : False
        """
        if self.chain.__len__() == 1:
            if self.chain[0].previous_hash != self.chain[0].compute_hash():
                return False
            return True
        for i in range(1, self.chain.__len__()):
            block = self.chain[i]
            if block.hash != block.compute_hash():
                print("Data was manipulated")
                return False
            previous_block = self.chain[i-1]
            if previous_block.hash != block.previous_hash:
                print("Block chain broke")
        return True


if __name__ == "__main__":
    # block = Block("10", "")
    # block = block.__dict__
    # print(json.dumps(block, ensure_ascii=False, indent=4))
    coin = Chain(4)
    tx1 = Transaction("addr1", "addr2", 10)
    tx2 = Transaction("addr2", "addr2", 5)
    coin.add_transaction(tx1).add_transaction(tx2)
    print(json.dumps(coin, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    coin.mine_transaction_pool("addr3")

    print(json.dumps(coin, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    # print(json.dumps(coin, indent=4))
    # chains.difficulty = 5
    # block1 = Block("Transfer 10 yuan", "")
    # chains.add_block(block1)
    # print(chains.get_latest_block().hash)
    # block2 = Block("Transfer 20 yuan", "")
    # chains.add_block(block2)
    # print(chains.get_latest_block().hash)

    # for chain in chains.chain:
    #     print(json.dumps(chain.__dict__, ensure_ascii=False, indent=4))
    # print(chains.validate())

    # 篡改第一个block的data
    # chains.chain[1].data = "Transfer 100 yuan"
    # chains.chain[1].hash = chains.chain[1].compute_hash()
    # print(chains.validate())
