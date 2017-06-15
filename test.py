import resource

rsrc = resource.RLIMIT_DATA
soft, hard = resource.getrlimit(rsrc)
print 'Soft limit starts as  :', soft
print "hard limit starts as :", hard
