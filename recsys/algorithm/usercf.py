#! /usr/bin/env python
#-*- coding: utf-8 -*-

class UserCF():
  """
  Use user-cf algorithm to recommend
  
  Attributes:
  _matrix: the user-item matrix contain the score by user, an instance of recsys.utils.sparse_matrix.DictMatrix.
  _user_similar: instance of UserSimilar
  """ 
  
  #static final value for use different similar algorithm
  USER_SIMILAR = 0                           #UserSimilar
  HERLOCKER_USER_SIMILAR = 1       #HerlockerUserSimilar  
  
  def __init__(self, matrix, similar = 0):
    """
    init method
        
    Args:
        matrix: the user-item matrix contain the score by user. 
                        matrix is an instance of recsys.utils.sparse_matrix.DictMatrix.
                        if you make sure matrix's index i and j is continuous from 0, the compute speed while be fast. 
    """      
    self._matrix = matrix
    self._avg = {}
    if similar == UserCF.USER_SIMILAR:
      from recsys.similarity.user_similar import UserSimilar
      self._user_similar = UserSimilar(matrix)
    elif similar == UserCF.HERLOCKER_USER_SIMILAR:
      from recsys.similarity.herlocker_user_similar import HerlockerUserSimilar
      self._user_similar = HerlockerUserSimilar(matrix)
  
  def prediction(self, user, item):
    """
    get prediction of user-item pair by user-cf
    prediciton(a, p) = avg_a + sum( sim(a,b) * (r(b,p) - avg_b) / sum(sim(a,b))
        
    Args:
        user: user index
        item: item index
    """          
    # if user have rate the item
    if self._matrix[user, item] != 0:
      return self._matrix[user, item]
    
    # else
    topN = self._user_similar.topN(user, item, 50)
    avg_u = self._userAverage(user)
    count = 0.0
    weights = 0.0
    for i in topN:
      count += (self._matrix[i[0], item] - self._userAverage(i[0])) * i[1]
      weights += i[1]
    if weights == 0:
      return avg_u
    return avg_u + count / weights

  def _userAverage(self, user):
    """
    compute the average rate of user
        
    Args:
        user: user index
    """          
    try:
      return self._avg[user]
    except:
      avg = self._average(self._matrix[user, ...])
      self._avg[user] = avg
      return avg

  def _average(self, vec):
    """
    compute the average of vec
        
    Args:
        vec: dictionary with key-index, value-rate 
    """       
    vec_len = max(vec.keys())+1
    total = 0.0
    count = 0
    for i in range(vec_len):
      try:
        if vec[i] <> 0:
          total += vec[i]
          count += 1
      except:
        pass
    if count == 0:
      return 0
    return total/count
    