from abc import ABC, abstractmethod

from django.shortcuts import redirect


class BaseAuthenticator(ABC):

  _AUTHENTICATORS : dict[str, "BaseAuthenticator"] = dict() 

  @abstractmethod
  def authenticate(self, request, callback_path):
    raise NotImplementedError()
  
  @abstractmethod
  def authenticate_callback(self, request):
    raise NotImplementedError()
  
  @abstractmethod
  def get_identifier(self, request):
    raise NotImplementedError()
  
  @abstractmethod
  def is_logged_in(self, request):
    raise NotImplementedError()
  
  def RegisterInstance(name : str, auth : "BaseAuthenticator"):
    BaseAuthenticator._AUTHENTICATORS[name] = auth

  def GetInstance(name : str) -> "BaseAuthenticator":
    return BaseAuthenticator._AUTHENTICATORS[name]
