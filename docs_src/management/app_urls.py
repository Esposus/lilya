from lilya.routing import Include

route_patterns = [Include("/api/v1", namespace="accounts.v1.urls")]
