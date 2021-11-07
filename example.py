from abc import ABCMeta, abstractmethod


class LoggerBase(metaclass=ABCMeta):
    info = 0
    error = 1
    next = None

    def setNext(self, next):
        self.next = next
        return next
    
    @abstractmethod
    def call(self,message: str, loggerType: int):
        pass


class Logger(LoggerBase):

    def call(self, message: str, loggerType: int):
        if loggerType == self.info:
            print('Logger:',message)
        
        if self.next:
            self.next.call(message, loggerType)


class FileLogger(LoggerBase):

    def call(self, message: str, loggerType: int):
        if loggerType == self.error:
            print('FileLogger:', message)
        
        if self.next:
            self.next.call(message, loggerType)


class ErrorHandler:
    next = None

    def setNext(self, next):
        self.next = next
        return next

    def call(self, *args):
        try:
            if self.next:
                self.next.call(*args)
        except Exception as e:
            print(e)


class SlackNotifer(LoggerBase):
    
    def call(self, *args):
        if args[1] == self.error:
            print('Slack:', args[0])

        if self.next:
            self.next.call(*args)


LOGGER = Logger()
FILE_LOGGER = FileLogger()

LOGGER.setNext(FILE_LOGGER)
LOGGER.call('コンソールに出力されるログです', 0)
LOGGER.call('重大なエラーが発生しました', 1)

ROOT = ErrorHandler()
SLACK_NOTIFER = SlackNotifer()

ROOT.setNext(LOGGER).setNext(FILE_LOGGER).setNext(SLACK_NOTIFER)

ROOT.call('コンソールに出力されるログです', 0)
ROOT.call('重大なエラーが発生しました', 1)