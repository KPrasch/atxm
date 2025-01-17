from enum import Enum

from web3.types import PendingTx, RPCError, TxReceipt


class Fault(Enum):
    """
    Fault codes for transaction processing.
    These are alternate states that a transaction can enter
    other than "finalized".
    """

    # Strategy has been running for too long
    TIMEOUT = "timeout"

    # Transaction has been capped and subsequently timed out
    PAUSE = "pause"

    # Transaction reverted
    REVERT = "revert"

    # Something went wrong
    ERROR = "error"

    # ...
    INSUFFICIENT_FUNDS = "insufficient_funds"


class InsufficientFunds(RPCError):
    """raised when a transaction exceeds the spending cap"""


class Wait(Exception):
    """
    Raised when a strategy exceeds a limitation.
    Used to mark a pending transaction as "wait, don't retry".
    """


class TransactionFaulted(Exception):
    """Raised when a transaction has been faulted."""

    def __init__(self, tx: PendingTx, fault: Fault, message: str):
        self.tx = tx
        self.fault = fault
        self.message = message
        super().__init__(message)


class TransactionReverted(TransactionFaulted):
    """Raised when a transaction has been reverted."""

    def __init__(self, tx: PendingTx, receipt: TxReceipt, message: str):
        self.receipt = receipt
        super().__init__(tx=tx, fault=Fault.REVERT, message=message)
