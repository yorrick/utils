
# colors
# export TERM="xterm-color"
# export PS1="\e[1;30m\][\e[\e[1;30m\]\e[1;33m\] \u@\H \[\e[1;32m\]\w\[\e[0m\] \e[1;30m\]]\n[\[ \e[1;31m\]\T\[\e[0m\]\e[1;30m\] ] > \e[37m\]"
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

# makes brew installed software before others
PATH=/usr/local/bin:$PATH
export PATH

# work
WORKDIR=~/work
export WORKDIR

# python path
# PYTHONPATH=$PYTHONPATH:$WORKDIR/voiturolio/lib/django/
# PYTHONPATH=$PYTHONPATH:$WORKDIR/
# PYTHONPATH=$PYTHONPATH:$WORKDIR/x
# PYTHONPATH=$PYTHONPATH:$WORKDIR/x/xt
# export PYTHONPATH

# aliases
alias ll='ls -la'
alias cleanpyc='find . -type f -name "*.pyc" -exec rm -f {} \;'
# alias ls='ls $LS_OPTIONS -hF'
# alias ll='ls $LS_OPTIONS -lAhF'
# alias cdwork='cd $WORKDIR'

# restaure sessions by tab for iterm2
export HISTFILE=~/.bash-history-${ITERM_SESSION_ID}


# ssh completion
_complete_ssh_hosts ()
{
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    comp_ssh_hosts=`cat ~/.ssh/config  | grep "^Host " | awk '{print $2}'`
    COMPREPLY=( $(compgen -W "${comp_ssh_hosts}" -- $cur))
    return 0
}
complete -F _complete_ssh_hosts ssh

# Bash completion 
if [ -f `brew --prefix`/etc/bash_completion ]; then
    . `brew --prefix`/etc/bash_completion
fi

# Git completion
source ~/.git-completion.bash

# nice git tips in PS1
# https://gist.github.com/921364

function git_branch {
    ref=$(git symbolic-ref HEAD 2> /dev/null) || return;
    echo "("${ref#refs/heads/}") ";
}

function git_since_last_commit {
    now=`date +%s`;
    last_commit=$(git log --pretty=format:%at -1 2> /dev/null) || return;
    seconds_since_last_commit=$((now-last_commit));
    minutes_since_last_commit=$((seconds_since_last_commit/60));
    hours_since_last_commit=$((minutes_since_last_commit/60));
    minutes_since_last_commit=$((minutes_since_last_commit%60));
                                
    echo "${hours_since_last_commit}h${minutes_since_last_commit}m ";
}

PS1="[\[\033[1;32m\]\w\[\033[0m\]]\[\033[0m\]\[\033[1;36m\]\$(git_branch)\[\033[0;33m\]\$(git_since_last_commit)\[\033[0m\]$ "

source ~/.django_bash_completion.bash

