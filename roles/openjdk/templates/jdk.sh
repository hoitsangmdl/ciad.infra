export JAVA_HOME=$(readlink -f /usr/bin/javac | sed "s:bin/javac::")
export JRE_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")

