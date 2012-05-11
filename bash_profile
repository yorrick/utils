
# colors
# export TERM="xterm-color"
# export PS1="\e[1;30m\][\e[\e[1;30m\]\e[1;33m\] \u@\H \[\e[1;32m\]\w\[\e[0m\] \e[1;30m\]]\n[\[ \e[1;31m\]\T\[\e[0m\]\e[1;30m\] ] > \e[37m\]"
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

##
# Your previous /Users/yorrick/.bash_profile file was backed up as /Users/yorrick/.bash_profile.macports-saved_2011-10-18_at_08:59:57
##

# MacPorts Installer addition on 2011-10-18_at_08:59:57: adding an appropriate PATH variable for use with MacPorts.
PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

# Adds postgres binaries to path
PATH=$PATH:/Library/PostgreSQL/9.1/bin/

# adds scala to path
PATH=$PATH:~/scala/bin
PATH=$PATH:/usr/local/sbin


export PATH

# work
WORKDIR=~/Work
export WORKDIR

# python path
# PYTHONPATH=$PYTHONPATH:$WORKDIR/voiturolio/lib/django/
# PYTHONPATH=$PYTHONPATH:$WORKDIR/
# PYTHONPATH=$PYTHONPATH:$WORKDIR/x
# PYTHONPATH=$PYTHONPATH:$WORKDIR/x/xt
# export PYTHONPATH

# aliases
alias ll='ls -la'
alias voiturolio='source ~/virtualenvs/voiturolio/bin/activate'
alias voiturolio-django14='source ~/virtualenvs/voiturolio-django14/bin/activate'
alias cleanpyc='find . -type f -name "*.pyc" -exec rm -f {} \;'
# alias ls='ls $LS_OPTIONS -hF'
# alias ll='ls $LS_OPTIONS -lAhF'
# alias cdwork='cd $WORKDIR'

# restaure sessions by tab for iterm2
export HISTFILE=~/.bash-history-${ITERM_SESSION_ID}

# Git completion
source ~/.git-completion.bash

function parse_git_branch_and_add_brackets {
  git branch --no-color 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\ \[\1\]/'
}
PS1="\h:\W\[\033[0;32m\]\$(parse_git_branch_and_add_brackets)\[\033[0m\] \$ "
